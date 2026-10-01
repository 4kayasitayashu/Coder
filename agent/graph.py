from dotenv import load_dotenv
from langgraph.graph import *
from langgraph.constants import END
from langchain.agents import create_agent
# from langchain_groq.chat_models import ChatGroq
from llm.factory import get_llm, invoke_structured
from agent.prompts import *
from agent.tools import *
from agent.states import  *
import json, os
load_dotenv()

# set_debug(True)
#set_verbose(True)
# planner_llm = ChatGroq(model="openai/gpt-oss-120b",
#                temperature=0)
# architect_llm = ChatGroq(model="openai/gpt-oss-120b",
#                temperature=0)
# coder_llm = ChatGroq(model="openai/gpt-oss-120b",
#                temperature=0)
# reviewer_llm = ChatGroq(model="openai/gpt-oss-20b",
#                temperature=0)
# fixer_llm = ChatGroq(model="openai/gpt-oss-120b",
#                temperature=0)
# tester_llm = ChatGroq(model="openai/gpt-oss-120b",
#                temperature=0)



def planner_agent(state: dict) -> dict:
    """Converts user prompt into a structured Plan"""
    user_prompt = state["user_prompt"]
    resp = invoke_structured(Plan, planner_prompt(user_prompt), agent_name="planner")
    if resp is None:
        raise ValueError("Planner did not return a valid response.")
    return {"plan": resp, "user_prompt":user_prompt}

def architect_agent(state: dict) -> dict:
    """"Creates TaskPlan from Plan"""
    plan:Plan = state["plan"]
    resp=invoke_structured(TaskPlan, architect_prompt(plan=plan.model_dump_json(indent=2)), agent_name="architect")
    if resp is None:
        raise ValueError("Architect did not return a valid response.")
    resp.plan=plan
    # print(resp.model_dump_json())
    return {"task_plan": resp,  "user_prompt": state["user_prompt"]}

def coder_agent(state: dict) -> dict:
    """Langgraph tool-using coder agent"""
    coder_state:CoderState = state.get("coder_state")
    if coder_state is None:
        coder_state= CoderState(user_prompt=state["user_prompt"],task_plan=state["task_plan"],current_step_idx=0)
    steps = coder_state.task_plan.implementation_steps
    if coder_state.current_step_idx >= len(steps):
        return {
        "coder_state": coder_state,
        "status": "DONE",
        "user_prompt": state["user_prompt"]
    }
    current_task= steps[coder_state.current_step_idx]
    existing_content=read_file.invoke({"path": current_task.filepath})
    system_prompt=coder_system_prompt()
    user_prompt=(
        f"Task: {current_task.task_description}\n"
        f"File: {current_task.filepath}\n"
        f"Existing content: \n{existing_content}\n"
        "Use write_file(path,content) to save your changes."
    )
    coder_tools=[read_file,write_file,list_files,get_current_directory]
    llm=get_llm(agent_name="coder")
    react_agent=create_agent(llm,coder_tools)
    for attempt in range(3):
        try:
            result=react_agent.invoke({"messages":     
                                [{"role":"system","content":system_prompt},
                                    {"role":"user","content":user_prompt}]})
            print(result)
            # content = read_file.invoke({"path": current_task.filepath})
            p = PROJECT_ROOT/current_task.filepath
            if p.exists():
                if current_task.filepath not in coder_state.generated_files:
                    coder_state.generated_files.append(current_task.filepath)
            coder_state.current_step_idx+=1
            status = "DONE" if coder_state.current_step_idx >= len(steps) else "CODING"
            return {
    "coder_state": coder_state,
    "status": status,
    "user_prompt": state["user_prompt"]
}
        except Exception as e:
            print(f"Coder step failed for {current_task.filepath}: {e}")
    return {"coder_state":coder_state, "status":"FAILED","user_prompt": state["user_prompt"]}

def review_agent(state: dict)-> dict:
    """Code review agent"""
    coder_state: CoderState = state["coder_state"]
    task_plan = coder_state.task_plan
    project_code =""
    for file in coder_state.generated_files:
        content=read_file.invoke({"path":file})
        project_code+= (f"===={file}====\n{content}\n")
    result = invoke_structured(ReviewResult, reviewer_prompt(task_plan, project_code), agent_name="reviewer")
    print(result.model_dump_json(indent=2))
    return {"coder_state":coder_state,"review_result": result,"user_prompt": state["user_prompt"]}

def fixer_agent(state: dict):
    coder_state = state["coder_state"]
    review_result = state["review_result"]
    project_code = ""
    for file in coder_state.generated_files:
        project_code += (
            f"\n===== {file} =====\n"
            + read_file.invoke({"path": file})
        )
    if review_result.approved:
        return {
            "coder_state": coder_state,
            "fix_status": "SKIPPED", 
            "user_prompt": state["user_prompt"]
        }
    coder_state.fix_attempts += 1
    fix_tools = [read_file,write_file, list_files,get_current_directory]
    llm=get_llm(agent_name="fixer")
    react_agent=create_agent(llm,fix_tools)
    for attempt in range(3):
        try:
            react_agent.invoke({
        "messages" :[{
            "role":"system",
            "content":"You are a software maintenance engineer."
        },
        {
            "role":"user",
            "content": fixer_prompt(coder_state.task_plan,review_result, project_code)
        }
        ]
    })
        # print(result)
            return{
        "coder_state": coder_state,
        "fix_status": "DONE",
        "user_prompt": state["user_prompt"]
    }
        except Exception as e:
            print(f"Fixer attempt {attempt+1} failed: {e}")
    return{
        "coder_state":coder_state,
        "fix_status":"FAILED",
        "user_prompt": state["user_prompt"]
    }

    
def executor_agent(state: dict)->dict:
    coder_state = state["coder_state"]
    tech = coder_state.task_plan.plan.techstack.lower()
    if "python" in tech:
        code, out, err = run_cmd.invoke({
            "cmd": "python main.py"
        })
    elif "react" in tech:
        code, out, err = run_cmd.invoke({
            "cmd": "npm install && npm run build"
        })
    elif "html" in tech:
        return {
            "coder_state":coder_state,
            "execution_result": ExecutionResult(
                success=True,
                exit_code=0,
                stdout="Static project - execution skipped.",
                stderr=""
            ),
            "user_prompt": state["user_prompt"],
            "review_result": state.get("review_result")
        }
    else:
        code, out, err = 1, "", f"Unsupported tech stack: {tech}"
    return {
        "coder_state":coder_state,
        "execution_result": ExecutionResult(
            success=(code == 0),
            exit_code=code,
            stdout=out,
            stderr=err
        ),
        "user_prompt": state["user_prompt"],
        "review_result": state.get("review_result")
    }

def tester_agent(state: dict):
    coder_state = state["coder_state"]
    project_code = ""
    for file in coder_state.generated_files:
        project_code += (
            f"\n\n===== {file} =====\n"
            + read_file.invoke({"path": file})
        )
    try:
        result = invoke_structured(
            TestResult,
            tester_prompt(
                coder_state.user_prompt,
                coder_state.task_plan,
                project_code,
                state["execution_result"]
            ),
            agent_name="tester"
        )
        if result is None:
            raise ValueError("Tester did not return a valid response.")
    except Exception as e:
        print(f"Tester failed to produce valid output: {e}")
        result = TestResult(passed=False, suggestions=[f"Tester failed to produce valid output: {e}"])
    coder_state.test_attempts += 1
    git_status = None
    if result.passed:
        git_status = auto_git_push(
        message=f"Auto-generated project: {coder_state.user_prompt}"
    )

    return {
        "coder_state":coder_state,
        "test_result": result,
        "git_status": git_status,
        "user_prompt": state["user_prompt"],
        "review_result": state.get("review_result")
    }
    
def publisher_agent(state: dict):
    coder_state = state["coder_state"]
    PROJECT_DIR= PROJECT_ROOT 
    repo_url = os.getenv("GENERATED_PROJECT_REMOTE_URL")
    cmds = [
        "git add .",
        f'git commit -m "Initial commit: {coder_state.user_prompt}"',
        "git branch -M main",
        "git push -u origin main",
    ]
    optional_cmds = [
    "git pull origin main --allow-unrelated-histories --no-edit",
]
    final_cmds = [
    "git push -u origin main",
]
    logs = []
    if not (PROJECT_DIR / ".git").exists():
        run_cmd.invoke({"cmd":"git init","cwd":str(PROJECT_DIR)})
    if repo_url and not has_git_remote():
        run_cmd.invoke({"cmd": f"git remote add origin {repo_url}", "cwd": str(PROJECT_DIR)})
    for cmd in cmds:
        code, out, err = run_cmd.invoke({"cmd": cmd,"cwd": str(PROJECT_DIR)})
        logs.append({
            "cmd": cmd,
            "exit_code": code,
            "stdout": out,
            "stderr": err
        })
        if code != 0:
            return {
                "coder_state": coder_state,
                "publish_status": "FAILED",
                "publish_logs": logs,
                "user_prompt": state["user_prompt"]
            }
    for cmd in optional_cmds:
        code, out, err = run_cmd.invoke({"cmd": cmd, "cwd": str(PROJECT_DIR)})
        logs.append({"cmd": cmd, "exit_code": code, "stdout": out, "stderr": err})
    for cmd in final_cmds:
        code, out, err = run_cmd.invoke({"cmd": cmd, "cwd": str(PROJECT_DIR)})
        logs.append({"cmd": cmd, "exit_code": code, "stdout": out, "stderr": err})
    coder_state.published = True
    return {
        "coder_state": coder_state,
        "publish_status": "DONE",
        "publish_logs": logs,
        "user_prompt": state["user_prompt"]
    }
    
graph=StateGraph(dict)
graph.add_node("planner",planner_agent)
graph.add_node("architect",architect_agent)
graph.add_node("coder",coder_agent)
graph.add_node("reviewer",review_agent)
graph.add_node("fixer",fixer_agent)
graph.add_node("executor", executor_agent)
graph.add_node("tester", tester_agent)
graph.add_node("publisher", publisher_agent)
graph.add_conditional_edges(
    "reviewer",
    lambda s: ("executor" if s["review_result"].approved else "fixer" if s["coder_state"].fix_attempts<3 else "executor"),
    {
        "executor": "executor",
        "fixer": "fixer",
    }
)
graph.add_edge("planner","architect")
graph.add_edge("architect","coder")
graph.add_edge("fixer","reviewer")
graph.add_edge("executor", "tester")
graph.add_edge("publisher",END)
graph.add_conditional_edges(
    "coder",
    lambda s: "reviewer" if s.get("status") == "DONE"  else "coder",
    {"reviewer": "reviewer", "coder": "coder"}
)
graph.add_conditional_edges(
    "tester",
    lambda s: (
        "publisher"
        if s["test_result"].passed
        else "fixer"
        if s["coder_state"].test_attempts < 2
        else "END"
    ),
    {
        "publisher": "publisher",
        "fixer": "fixer",
        "END":END
    }
)

graph.set_entry_point("planner")
agent=graph.compile()

if __name__=="__main__":
    result = agent.invoke({"user_prompt": "Build a colourful modern todo app in html css and js"},
                          {"recursion_limit": 100})
    print("Final State:", result)
