import os
from openai import OpenAI
from dotenv import load_dotenv
from langchain_community.utilities import WikipediaAPIWrapper

load_dotenv()

class ResearchAgent:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.wiki = WikipediaAPIWrapper()

    def build_prompt(self, keyword: str, wiki_context: str) -> str:
        return f"""
        You are a senior research expert known for conducting comprehensive, structured, and academically sound research.

        You follow professional research principles to ensure quality, accuracy, and real-world relevance.

        Below is background context from Wikipedia:
        \"\"\"
        {wiki_context}
        \"\"\"

        Write a detailed research report on the topic: "{keyword}" using the following exact headings. Each section should be informative and structured. If you don’t have enough information for any section, return "None".

        1. Defining the Scope
        2. Research Design
        3. Literature Review
        4. Data Analysis
        5. Discussion and Conclusion
        6. Ethical Considerations
        7. References
        """

    def extract_section(self, content: str, section: str, next_section: str = None) -> str:
        if section not in content:
            return None
        start = content.find(section)
        end = content.find(next_section) if next_section and next_section in content else None
        section_text = content[start + len(section):end].strip() if end else content[start + len(section):].strip()

        cleaned = section_text.replace("##", "").strip()
        if cleaned.lower() == "none" or not cleaned:
            return None
        return cleaned

    def research(self, keyword: str) -> dict:
        context = self.wiki.run(keyword)
        prompt = self.build_prompt(keyword, context)

        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.4,
            max_tokens=2000
        )

        content = response.choices[0].message.content.strip()

        return {
            "keyword": keyword,
            "scope": self.extract_section(content, "1. Defining the Scope", "2. Research Design"),
            "design": self.extract_section(content, "2. Research Design", "3. Literature Review"),
            "literature": self.extract_section(content, "3. Literature Review", "4. Data Analysis"),
            "analysis": self.extract_section(content, "4. Data Analysis", "5. Discussion and Conclusion"),
            "discussion": self.extract_section(content, "5. Discussion and Conclusion", "6. Ethical Considerations"),
            "ethics": self.extract_section(content, "6. Ethical Considerations", "7. References"),
            "references": self.extract_section(content, "7. References")
        }
