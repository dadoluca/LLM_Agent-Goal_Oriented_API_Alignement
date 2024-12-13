# LLM Agent - Goal Oriented API Alignement

## Overview
This repository implements a system for aligning high-level goals with API endpoints using Goal-Oriented Requirements Engineering (GORE) techniques and Large Language Models (LLMs). The system extracts goals from natural language requirement documents, decomposes them into low-level goals, and maps them to corresponding API endpoints. The goal is to automate the process of translating system goals into actionable API calls for software applications.

## Features
- **Goal Extraction:** Extract high-level goals from natural language requirements documents (e.g., GitHub README files, requirement specifications).
- **Goal Decomposition:** Decompose high-level goals into low-level goals using a hierarchical approach.
- **API Mapping:** Map low-level goals to available API endpoints based on provided API documentation (e.g., Swagger files).
- **Integration with LLM Agents:** Leverages LLMs to automate goal modeling, decomposition, and mapping processes.

## Installation
1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/goals-api-alignment.git
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.
