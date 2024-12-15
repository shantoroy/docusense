# DocuSense

This is the main repository for DocuSense (NERDathon June '24 Cohort). 

DocuSense is a retrieval augmented generation (RAG) system built with TypeScript + React, Python (Flask), and open-source large language models (LLMs). 

## Brief Description of the System
1. Documents are transformed into a vector representation and loaded into the system. 
2. User queries system. Their query is transformed into a vector. 
3. Calculate dot product between vectors to find similarity. 
4. Find top n documents, pass into LLM along with engineered prompt. 
5. Return LLM response with citations to the user. 

## Technical Information
- Open-source models obtained from HuggingFace. 
- Text embedding model: `Snowflake/snowflake-arctic-embed-l`
- Large language model: `google/gemma-2-2b-it`

## Directory Structure
- `./DocuSense-Frontend`: Frontend UI code
- `./DocuSense-Backend`: Backend code (webserver)
- `./demo-data`: A preview of the data that was loaded into the RAG system. 
