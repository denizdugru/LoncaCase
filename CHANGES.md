## Unreleased

### Feat

- **llm_parser**: added llm support for keyword correction and also xlm parser to the desired schema(experimental)
- **periodic_task_py**: added a xml parser without uvicorn app
- **logging**: added stdout support for logging
- **logging**: added logger to track the processes better, minor changes
- **file_upload**: added support to upload files
- **config**: added new env file configurations to easily access variables, added new logic to convert variables to float
- **mongo**: integrated mongoengine, implemented creation of the docs and other utilities
- **precommit**: added precommit hook for debug statements
- **pre_commit**: added precommit config file, added .gitignore, black linted

### Fix

- **requirements**: fixed requirements errors

### Refactor

- **file_names**: changed file and folder names to more suitable ones
