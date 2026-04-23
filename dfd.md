# Data Flow Diagrams (DFD)

Here are the Data Flow Diagrams representing the flow of information within the `ProjectHub` system.

## Level 0 Context Diagram
The context diagram shows the system as a single high-level process with its interactions with external entities (Users).

```mermaid
flowchart TD
    %% External Entities
    Teacher[/"Teacher"\]
    Student[/"Student"\]

    %% System
    ProjectHub((ProjectHub\nSystem))

    %% Data Flows - Teacher
    Teacher -- "Creates Projects\nViews Analytics\nReviews Submissions" --> ProjectHub
    ProjectHub -- "Project Status\nStudent Progress\nEvaluation Summaries" --> Teacher

    %% Data Flows - Student
    Student -- "Joins Projects & Groups\nSubmits Tasks & Projects\nRates Peers\nSends Messages" --> ProjectHub
    ProjectHub -- "Task Assignments\nGroup Details\nDeadlines\nProject Updates" --> Student
```

## Level 1 DFD
The Level 1 DFD breaks down the main system into major sub-processes and shows the data stores they interact with.

```mermaid
flowchart TD
    %% External Entities
    Teacher[/"Teacher"\]
    Student[/"Student"\]

    %% Processes
    P1(("1\nUser &\nProfile\nManagement"))
    P2(("2\nProject\nManagement"))
    P3(("3\nGroup\nManagement"))
    P4(("4\nTask &\nSubmission\nManagement"))
    P5(("5\nCommunication\nManagement"))
    P6(("6\nPeer\nEvaluation"))

    %% Data Stores
    D1[(D1: Users & Profiles)]
    D2[(D2: Projects & Members)]
    D3[(D3: Groups & Members)]
    D4[(D4: Tasks & Submissions)]
    D5[(D5: Messages)]
    D6[(D6: Team Ratings)]

    %% Flows - User Management
    Teacher & Student -- "Registration Info\nCredentials" --> P1
    P1 -- "Auth Token\nProfile Data" --> Teacher & Student
    P1 <--> |Read/Write| D1

    %% Flows - Project Management
    Teacher -- "Project Details\nDeadlines" --> P2
    Student -- "Join Codes" --> P2
    P2 -- "Project Info" --> Teacher & Student
    P2 <--> |Read/Write| D2

    %% Flows - Group Management
    Student -- "Create Group\nJoin Group" --> P3
    P3 -- "Group Assignments" --> Student
    P3 <--> |Read/Write| D3
    D2 -.-> |Validate Project| P3

    %% Flows - Task Management
    Teacher -- "Create Tasks\nAssign Tasks" --> P4
    Student -- "Task Updates\nFile Submissions\nFinal Projects" --> P4
    P4 -- "Task Status\nFiles" --> Teacher & Student
    P4 <--> |Read/Write| D4
    D3 -.-> |Validate Group| P4

    %% Flows - Communication
    Student & Teacher -- "Messages" --> P5
    P5 -- "Chat History" --> Student & Teacher
    P5 <--> |Read/Write| D5
    D2 -.-> |Validate Membership| P5

    %% Flows - Peer Evaluation
    Student -- "Peer Ratings\nComments" --> P6
    P6 -- "Evaluation Results" --> Teacher
    P6 <--> |Read/Write| D6
    D3 -.-> |Validate Group Members| P6
```
