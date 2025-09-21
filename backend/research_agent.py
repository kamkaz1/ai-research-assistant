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

            CRITICAL SOURCE FORMATTING RULES:
            - Look for actual URLs in the search results and include them
            - Use EXACT format: [number] Title (URL)
            - Title should be the actual article/page title from the search results
            - URL must be a real web address from the search results (http:// or https://)
            - Copy URLs exactly as they appear in the search results
            - If you see URLs in the search results, you MUST include them
            - Do NOT use placeholder text like "Source title" or "no url"
            - Do NOT make up URLs - only use ones found in the search results
            - Make titles descriptive and specific to the content
            - Include at least 3 sources with real URLs if available in search results

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
                        source_title = ""
                        source_url = ""
                        
                        # Remove the [number] prefix first
                        if ']' in line:
                            content_after_bracket = line.split(']', 1)[1].strip()
                        else:
                            content_after_bracket = line.strip()
                        
                        # Now parse the content after the bracket
                        if '(' in content_after_bracket and ')' in content_after_bracket:
                            # Format: Title (URL)
                            url_start = content_after_bracket.find('(') + 1
                            url_end = content_after_bracket.find(')')
                            source_url = content_after_bracket[url_start:url_end].strip()
                            
                            # Extract title before the (
                            source_title = content_after_bracket[:content_after_bracket.find('(')].strip()
                        elif ' - ' in content_after_bracket:
                            # Format: Title - URL
                            parts = content_after_bracket.split(' - ', 1)
                            if len(parts) == 2:
                                source_title = parts[0].strip()
                                source_url = parts[1].strip()
                        else:
                            # Format: Title only (no URL)
                            source_title = content_after_bracket.strip()
                        
                        # Clean up and validate
                        if not source_title:
                            source_title = f"Source {len(sources) + 1}"
                        
                        # Validate URL
                        if source_url:
                            # Remove any invalid characters
                            source_url = source_url.replace(' ', '').replace('%20', '')
                            if not source_url.startswith(('http://', 'https://')):
                                if '.' in source_url:  # Looks like a domain
                                    source_url = 'https://' + source_url
                                else:
                                    source_url = ""  # Invalid URL
                        
                        # Only add if we have a meaningful title
                        if source_title and len(source_title) > 3:
                            sources.append({
                                "title": source_title,
                                "url": source_url
                            })
                            logger.info(f"Added source: '{source_title}' -> '{source_url}'")
                        else:
                            logger.warning(f"Skipping source with invalid title: '{source_title}'")
                        
                    except Exception as e:
                        logger.warning(f"Could not parse source line: '{line}'. Error: {e}")
                        # Don't add invalid sources
            
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
            
            # Always try to extract sources from search results as fallback or supplement
            if len(sources) < 3 and search_results:
                logger.info(f"Only {len(sources)} sources found, attempting to extract more from search results")
                try:
                    import re
                    # More comprehensive URL pattern
                    url_pattern = r'https?://[^\s<>"{}|\\^`\[\]]+(?:[^\s<>"{}|\\^`\[\]]*[a-zA-Z0-9])?'
                    found_urls = re.findall(url_pattern, str(search_results))
                    
                    # Remove duplicates while preserving order
                    unique_urls = []
                    seen = set()
                    for url in found_urls:
                        if url not in seen and len(url) > 10:  # Filter out very short URLs
                            unique_urls.append(url)
                            seen.add(url)
                    
                    logger.info(f"Found {len(unique_urls)} unique URLs in search results")
                    
                    for i, url in enumerate(unique_urls[:5]):  # Get up to 5 sources
                        # Try to extract a title from the context around the URL
                        url_pos = str(search_results).find(url)
                        if url_pos != -1:
                            # Get context before and after the URL
                            start = max(0, url_pos - 200)
                            end = min(len(str(search_results)), url_pos + 200)
                            url_context = str(search_results)[start:end]
                            
                            # Look for potential title patterns in the context
                            title = self._extract_title_from_context(url_context, url)
                            
                            # Only add if we have a meaningful title and valid URL
                            if title and len(title) > 5 and self._is_valid_url(url):
                                sources.append({
                                    "title": title,
                                    "url": url
                                })
                                logger.info(f"Extracted source from search results: '{title}' -> '{url}'")
                                
                                # Stop if we have enough sources
                                if len(sources) >= 3:
                                    break
                except Exception as e:
                    logger.warning(f"Failed to extract sources from search results: {e}")
            
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
    
    def _extract_title_from_context(self, context: str, url: str) -> str:
        """Extract a meaningful title from the context around a URL."""
        try:
            import re
            
            # Remove the URL from context to focus on surrounding text
            context_without_url = context.replace(url, "")
            
            # Look for title patterns in the context
            # Pattern 1: Text in quotes
            quote_pattern = r'"([^"]{10,100})"'
            quote_match = re.search(quote_pattern, context_without_url)
            if quote_match:
                return quote_match.group(1).strip()
            
            # Pattern 2: Text in parentheses
            paren_pattern = r'\(([^)]{10,100})\)'
            paren_match = re.search(paren_pattern, context_without_url)
            if paren_match:
                return paren_match.group(1).strip()
            
            # Pattern 3: Capitalized sentences
            sentence_pattern = r'([A-Z][^.!?]{10,100}[.!?])'
            sentence_matches = re.findall(sentence_pattern, context_without_url)
            if sentence_matches:
                # Return the longest sentence that looks like a title
                best_title = max(sentence_matches, key=len)
                if len(best_title) > 15:
                    return best_title.strip()
            
            # Pattern 4: Text before common separators
            separators = [' - ', ' | ', ' :: ', ' – ']
            for sep in separators:
                if sep in context_without_url:
                    parts = context_without_url.split(sep)
                    if len(parts) > 1:
                        potential_title = parts[0].strip()
                        if len(potential_title) > 10:
                            return potential_title
            
            # Fallback: extract domain name from URL
            domain_match = re.search(r'https?://(?:www\.)?([^/]+)', url)
            if domain_match:
                domain = domain_match.group(1)
                return f"Article from {domain}"
            
            return "Source"
            
        except Exception as e:
            logger.warning(f"Failed to extract title from context: {e}")
            return "Source"
    
    def _is_valid_url(self, url: str) -> bool:
        """Validate if a URL is properly formatted and accessible."""
        try:
            import re
            # Basic URL validation
            url_pattern = r'^https?://[^\s<>"{}|\\^`\[\]]+\.[a-zA-Z]{2,}(?:/[^\s<>"{}|\\^`\[\]]*)?$'
            if not re.match(url_pattern, url):
                return False
            
            # Check for common invalid patterns
            invalid_patterns = [
                r'no%20url',
                r'example\.com',
                r'placeholder',
                r'http://$',
                r'https://$',
                r'\.\.\.',
                r'%20%20'
            ]
            
            for pattern in invalid_patterns:
                if re.search(pattern, url, re.IGNORECASE):
                    return False
            
            # Check URL length (not too short, not too long)
            if len(url) < 15 or len(url) > 500:
                return False
            
            return True
            
        except Exception as e:
            logger.warning(f"URL validation failed for {url}: {e}")
            return False


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
