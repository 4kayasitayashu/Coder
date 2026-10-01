from pydantic import BaseModel,Field,ConfigDict
from typing import Optional,Literal

class File(BaseModel):
    path: str= Field(description="The path of the file to be created")
    purpose: str= Field(description="The purpose of the file e.g., 'Main application logic','data preprocessing module' etc.")

class Plan(BaseModel):
    name: str= Field(description="The name of the application to be built")
    description: str= Field(description="A oneline description of the app to be built, e.g. 'A web application for managing personal finances'")
    techstack: str = Field(description="The tech stack to be used for the app, e.g. 'python', 'javascript', 'react', 'flask', etc.")
    features: list[str] = Field(description="A list of features that the app should have, e.g. 'user authentication', 'data visualization', etc.")
    files: list[File] = Field(description="A list of files to be created, each with a 'path' and 'purpose'")

class ImplementationTask(BaseModel):
    filepath: str= Field(description="The path of the file to be created")
    task_description: str= Field(description="A detailed description of the task to be performed on the file, e.g. 'add user authentication', 'implement data processing logic', etc.")

class TaskPlan(BaseModel):
    implementation_steps: list[ImplementationTask] = Field(description="A list of steps to be taken to implement the task")
    model_config = ConfigDict(extra="allow")

class CoderState(BaseModel):
    task_plan: TaskPlan = Field(description="The plan for the task to be implemented")
    current_step_idx: int = Field(0, description="The index of the current step in the implementation steps")
    generated_files: list[str] = Field(
        default_factory=list,
        description="List of generated files"
    )
    current_file_content: Optional[str] = Field(None, description="The content of the file currently being edited or created")
    fix_attempts: int = Field(
        0,
        description="Number of times Fixer has attempted to repair the project"
    )
    test_attempts: int = Field(
    0,
    description="Number of automatic testing retries"
    )
    published: bool = False
    user_prompt: str
  
class ReviewIssue(BaseModel):
    filepath: str
    issue: str
    severity: Literal["low", "medium", "high", "critical"]
    suggestion: str
    
class ReviewResult(BaseModel):
    approved: bool
    issues: list[ReviewIssue]
    # suggestions: list[str]

class ExecutionResult(BaseModel):
    success: bool
    exit_code: int
    stdout: str
    stderr: str

class TestResult(BaseModel):
    passed: bool
    failed_tests: list[str] = Field(default_factory=list)
    passed_tests: list[str] = Field(default_factory=list)
    suggestions: list[str]= Field(default_factory=list)