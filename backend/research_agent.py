import os
import logging
import json
from typing import Dict, List, Optional
from dotenv import load_dotenv
from langchain_community.utilities import SerpAPIWrapper
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ResearchAgent:
    """
    AI Research Assistant that combines web search with LLM processing
    to generate structured research notes with citations.
    """
    
    def __init__(self):
        """Initialize the research agent with LLM and search tools."""
        self._initialize_llm()
        self._initialize_search_tools()
        self._initialize_prompts()
        
    def _initialize_llm(self):
        """Initialize the Google Gemini language model."""
        google_api_key = os.getenv("GOOGLE_API_KEY")
        
        if not google_api_key:
            logger.error("GOOGLE_API_KEY not found in environment variables")
            raise ValueError("GOOGLE_API_KEY not found in environment variables.")
        
        logger.info(f"Found Google API key: {google_api_key[:10]}...")
        
        try:
            self.llm = ChatGoogleGenerativeAI(
                model="gemini-1.5-flash",
                temperature=0.1,
                google_api_key=google_api_key
            )
            logger.info("Initialized Google Gemini model")
        except Exception as e:
            logger.error(f"Failed to initialize Gemini model: {e}")
            raise ValueError(f"Failed to initialize Gemini model: {e}")
    
    def _initialize_search_tools(self):
        """Initialize search tools."""
        serpapi_api_key = os.getenv("SERPAPI_API_KEY")
        if not serpapi_api_key:
            logger.error("SERPAPI_API_KEY not found in environment variables")
            raise ValueError("SERPAPI_API_KEY not found in environment variables.")
        
        logger.info(f"Found SerpAPI key: {serpapi_api_key[:10]}...")
        
        try:
            self.search = SerpAPIWrapper(serpapi_api_key=serpapi_api_key)
            logger.info("Initialized SerpAPI search tool")
        except Exception as e:
            logger.error(f"Failed to initialize SerpAPI: {e}")
            raise ValueError(f"Failed to initialize SerpAPI: {e}")
    
    def _initialize_prompts(self):
        """Initialize prompt templates."""
        self.research_prompt_template = PromptTemplate.from_template(
            """You are a research assistant. Based on the search results below, create a research note.

            QUERY: {query}

            SEARCH RESULTS: {search_results}

            Create a research note with exactly this format:

            TITLE: [Write a clear title here]

            SUMMARY: [Write 3-5 sentences summarizing the key findings]

            KEY POINTS:
            - [First key point]
            - [Second key point]
            - [Third key point]
            - [Fourth key point]
            - [Fifth key point]

            SOURCES:
            [1] [Source title] ([URL])
            [2] [Source title] ([URL])
            [3] [Source title] ([URL])

            IMPORTANT: 
            - Extract actual source titles and URLs from the search results
            - Use the exact format: [number] Title (URL)
            - If no URL is available, use: [number] Title
            - Make sure source titles are descriptive and meaningful
            - Include at least 3 sources if available

            Be specific and use information from the search results."""
        )
    
    def run_research(self, query: str) -> Dict:
        """
        Perform comprehensive research on a given query.
        
        Args:
            query (str): The research query to investigate
            
        Returns:
            Dict: Structured research note with title, summary, key_points, and sources
            
        Raises:
            Exception: If research fails due to API errors or processing issues
        """
        try:
            logger.info(f"Starting research for query: {query}")
            
            # Validate input
            if not query or not query.strip():
                raise ValueError("Query cannot be empty")
            
            # Perform web search
            logger.info("Performing web search...")
            search_results = self.search.run(query)
            
            # Debug: Log search results
            logger.info(f"Search results length: {len(search_results) if search_results else 0}")
            logger.info(f"Search results preview: {search_results[:500] if search_results else 'None'}")
            
            if not search_results or search_results.strip() == "":
                logger.warning("No search results found")
                return self._create_empty_result(query, "No search results found for this query.")
            
            # Convert search results to string if it's a list
            if isinstance(search_results, list):
                search_results = " ".join(search_results)
            
            logger.info(f"Search completed. Processing results with LLM...")
            
            # Process with LLM
            chain = LLMChain(llm=self.llm, prompt=self.research_prompt_template)
            raw_output = chain.run(query=query, search_results=search_results)
            
            # Debug: Log LLM output before conversion
            logger.info(f"LLM output type: {type(raw_output)}")
            logger.info(f"LLM output: {raw_output}")
            
            # Extract the text content from the LLM response
            if hasattr(raw_output, 'content'):
                raw_output = raw_output.content
            elif isinstance(raw_output, dict) and 'text' in raw_output:
                raw_output = raw_output['text']
            else:
                raw_output = str(raw_output)
            
            # Debug: Log LLM output after conversion
            logger.info(f"LLM output length: {len(raw_output) if raw_output else 0}")
            logger.info(f"LLM output preview: {str(raw_output)[:1000] if raw_output else 'None'}")
            
            logger.info("LLM processing completed. Parsing results...")
            
            # Parse and structure the output
            parsed_output = self._parse_research_note(raw_output)
            
            # Debug: Log parsed output
            logger.info(f"Parsed output: {parsed_output}")
            
            # Validate the parsed output
            self._validate_research_output(parsed_output)
            
            logger.info(f"Research completed successfully for query: {query}")
            return parsed_output
            
        except Exception as e:
            logger.error(f"Research failed for query '{query}': {e}")
            raise
    
    def _parse_research_note(self, raw_text: str) -> Dict:
        """
        Parse the raw LLM output into a structured format.
        
        Args:
            raw_text (str): Raw output from the LLM
            
        Returns:
            Dict: Structured research note
        """
        try:
            title = "Research Results"
            summary = "No summary available"
            key_points = []
            sources = []
            
            # Debug: Log the raw text
            logger.info(f"Raw text to parse: {raw_text}")
            
            if not raw_text or len(raw_text.strip()) < 10:
                logger.warning(f"Raw text is too short: '{raw_text}'")
                return {
                    "title": title,
                    "summary": summary,
                    "key_points": key_points,
                    "sources": sources
                }
            
            lines = raw_text.split('\n')
            current_section = None
            summary_lines = []
            
            for line in lines:
                line = line.strip()
                
                # Debug: Log each line being processed
                logger.info(f"Processing line: '{line}' in section: {current_section}")
                
                # Detect section headers (case insensitive)
                if line.upper().startswith("TITLE:"):
                    title = line.replace("TITLE:", "").strip()
                    current_section = "title"
                    logger.info(f"Found title: {title}")
                elif line.upper().startswith("SUMMARY:"):
                    current_section = "summary"
                    summary_lines = []
                    logger.info("Found summary section")
                elif line.upper().startswith("KEY POINTS:"):
                    current_section = "key_points"
                    # Join accumulated summary lines
                    if summary_lines:
                        summary = " ".join(summary_lines).strip()
                        logger.info(f"Final summary: {summary}")
                elif line.upper().startswith("SOURCES:"):
                    current_section = "sources"
                    # Join accumulated summary lines if not done yet
                    if summary_lines and summary == "No summary available":
                        summary = " ".join(summary_lines).strip()
                        logger.info(f"Final summary from sources section: {summary}")
                elif line.upper().startswith("IMPORTANT GUIDELINES:"):
                    # Join accumulated summary lines if not done yet
                    if summary_lines and summary == "No summary available":
                        summary = " ".join(summary_lines).strip()
                        logger.info(f"Final summary from guidelines section: {summary}")
                    break  # Stop parsing after guidelines
                elif current_section == "summary" and line and not line.startswith(("-", "[", "TITLE:", "SUMMARY:", "KEY POINTS:", "SOURCES:", "IMPORTANT GUIDELINES:")):
                    summary_lines.append(line)
                    logger.info(f"Added to summary: {line}")
                elif current_section == "key_points" and line.startswith("-"):
                    point = line.replace("-", "").strip()
                    if point and len(point) > 10:  # Only add substantial points
                        key_points.append(point)
                        logger.info(f"Added key point: {point}")
                elif current_section == "sources" and line.startswith("["):
                    logger.info(f"Processing source line: '{line}'")
                    try:
                        # Parse source format: [1] Source Title (URL)
                        # Handle different formats: [1] Title (URL) or [1] Title - URL or [1] Title
                        source_title = "Source title unavailable"
                        source_url = ""
                        
                        # Extract title and URL
                        if '(' in line and ')' in line:
                            # Format: [1] Title (URL)
                            url_start = line.find('(') + 1
                            url_end = line.find(')')
                            source_url = line[url_start:url_end].strip()
                            
                            # Extract title between ] and (
                            title_start = line.find(']') + 1
                            title_end = line.find('(')
                            if title_start < title_end:
                                source_title = line[title_start:title_end].strip()
                        elif ' - ' in line:
                            # Format: [1] Title - URL
                            parts = line.split(' - ', 1)
                            if len(parts) == 2:
                                source_title = parts[0].split(']', 1)[1].strip() if ']' in parts[0] else parts[0].strip()
                                source_url = parts[1].strip()
                        else:
                            # Format: [1] Title (no URL)
                            if ']' in line:
                                source_title = line.split(']', 1)[1].strip()
                        
                        # Clean up title
                        if not source_title or source_title == "Source title unavailable":
                            source_title = f"Source {len(sources) + 1}"
                        
                        # Ensure URL is properly formatted
                        if source_url and not source_url.startswith(('http://', 'https://')):
                            source_url = 'https://' + source_url
                        
                        sources.append({
                            "title": source_title,
                            "url": source_url
                        })
                        logger.info(f"Added source: '{source_title}' -> '{source_url}'")
                        
                    except Exception as e:
                        logger.warning(f"Could not parse source line: '{line}'. Error: {e}")
                        # Fallback: add as-is
                        sources.append({
                            "title": f"Source {len(sources) + 1}",
                            "url": ""
                        })
                        logger.info(f"Added source (fallback): Source {len(sources)}")
            
            # Final check for summary
            if summary_lines and summary == "No summary available":
                summary = " ".join(summary_lines).strip()
                logger.info(f"Final summary from accumulated lines: {summary}")
            
            # Clean up summary
            if summary and summary != "No summary available":
                summary = summary.replace("SUMMARY:", "").strip()
            
            # If we still have no summary, try to extract from the raw text
            if summary == "No summary available":
                # Look for any substantial text that might be a summary
                text_parts = raw_text.split('\n\n')
                for part in text_parts:
                    if len(part.strip()) > 50 and not part.strip().startswith(('TITLE:', 'KEY POINTS:', 'SOURCES:', 'IMPORTANT')):
                        summary = part.strip()
                        logger.info(f"Extracted summary from text parts: {summary}")
                        break
            
            result = {
                "title": title,
                "summary": summary,
                "key_points": key_points,
                "sources": sources
            }
            
            logger.info(f"Final parsed result: {result}")
            return result
            
        except Exception as e:
            logger.error(f"Error in _parse_research_note: {e}")
            return {
                "title": "Research Results",
                "summary": "Error parsing research results",
                "key_points": [],
                "sources": []
            }
    
    def _validate_research_output(self, output: Dict) -> None:
        """
        Validate the research output structure.
        
        Args:
            output (Dict): The research output to validate
            
        Raises:
            ValueError: If output is invalid
        """
        required_fields = ["title", "summary", "key_points", "sources"]
        
        for field in required_fields:
            if field not in output:
                raise ValueError(f"Missing required field: {field}")
        
        if not output["title"] or output["title"] == "Research Results":
            logger.warning("Research title is generic or empty")
        
        if not output["summary"] or output["summary"] == "No summary available":
            logger.warning("Research summary is empty or generic")
        
        if not output["key_points"]:
            logger.warning("No key points found in research results")
        
        if not output["sources"]:
            logger.warning("No sources found in research results")
    
    def _create_empty_result(self, query: str, message: str) -> Dict:
        """
        Create an empty result when research fails.
        
        Args:
            query (str): The original query
            message (str): Error message
            
        Returns:
            Dict: Empty research result
        """
        return {
            "title": f"Research Results: {query}",
            "summary": message,
            "key_points": ["No key points available due to search failure"],
            "sources": []
        }


# Example usage and testing
if __name__ == "__main__":
    # Set up test environment variables
    if not os.getenv("GOOGLE_API_KEY"):
        print("Please set GOOGLE_API_KEY environment variable")
        exit(1)
    
    if not os.getenv("SERPAPI_API_KEY"):
        print("Please set SERPAPI_API_KEY environment variable")
        exit(1)
    
    try:
        agent = ResearchAgent()
        test_query = "latest advancements in artificial intelligence for healthcare"
        result = agent.run_research(test_query)
        
        print("=== RESEARCH RESULTS ===")
        print(f"Title: {result['title']}")
        print(f"Summary: {result['summary']}")
        print("\nKey Points:")
        for i, point in enumerate(result['key_points'], 1):
            print(f"{i}. {point}")
        print("\nSources:")
        for i, source in enumerate(result['sources'], 1):
            print(f"{i}. {source['title']} ({source['url']})")
            
    except Exception as e:
        print(f"Error during testing: {e}")
