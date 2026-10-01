from llm.factory import get_llm
from agent.states import TaskPlan   # <-- তোমার TaskPlan যেখানে আছে সেই actual path দাও


def main():
    llm = get_llm()

    structured_llm = llm.with_structured_output(TaskPlan)

    response = structured_llm.invoke(
        """
        Create a simple implementation plan for a Python CLI
        todo application.

        The application should support:
        - adding tasks
        - listing tasks
        - completing tasks
        - deleting tasks
        """
    )

    print(response)
    print(type(response))


if __name__ == "__main__":
    main()