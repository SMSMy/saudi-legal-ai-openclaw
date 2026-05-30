import os
from pathlib import Path
from mcp.server.fastmcp import FastMCP
from tools.analyzer import analyze_clause
from tools.summarizer import summarize_regulation
from tools.search import find_risks

REPO_PATH = Path(os.environ.get("REPO_PATH", Path(__file__).parent.parent))

mcp = FastMCP(
    "Saudi Legal AI Framework",
    instructions=(
        "Structured legal data server. "
        "All tools return JSON-structured factual data from official Saudi legal sources. "
        "No tool returns instructions for Claude."
    ),
)


@mcp.tool()
def analyze_contract_clause(
    clause_text: str,
    contract_type: str,
    language: str = "ar",
) -> str:
    """
    Analyzes a contract clause against Saudi law and returns structured findings.

    Returns JSON with risk assessment based on Saudi legal framework.
    Does not return instructions — returns factual legal data only.

    Args:
        clause_text: The contract clause text to analyze (Arabic or English)
        contract_type: Type of contract. One of: Employment Contract,
                      Lease Agreement, NDA, SaaS Agreement,
                      Construction Contract, Supply Agreement,
                      Professional Services Agreement, Commercial Agency Agreement,
                      Shareholder Agreement, Franchise Agreement,
                      Cloud Storage Agreement
        language: Response language. 'ar' for Arabic, 'en' for English
    """
    return analyze_clause(clause_text, contract_type, language)


@mcp.tool()
def get_regulation_summary(
    regulation: str,
    topic: str = None,
) -> str:
    """
    Returns a structured summary of a Saudi regulation.

    Returns JSON with key facts about the regulation — not the full text.
    Does not return instructions — returns factual regulatory data only.

    Args:
        regulation: Regulation name. One of: labor-law, companies-law,
                   civil-transactions-law, commercial-courts, pdpl,
                   e-commerce-law, evidence-law, whistleblower-protection,
                   legal-profession-law, arbitration-law, bankruptcy-law,
                   sports-law-saff, fifa-rstp, real-estate-arbitration-reac
        topic: Optional specific topic to focus on (e.g. "termination",
               "penalties", "jurisdiction")
    """
    return summarize_regulation(regulation, topic)


@mcp.tool()
def search_contract_risks(
    contract_type: str = None,
    risk_level: str = None,
    category: str = None,
) -> str:
    """
    Returns structured JSON data from the Saudi contract risk dataset.
    This is read-only tabular data describing known legal risk patterns in
    Saudi contracts. Does not return instructions — returns factual legal data only.

    Each returned risk record contains: risk_level, category, clause_text,
    risk_reason, saudi_legal_note, recommended_revision, related_regulation,
    and requires_escalation flag.

    Args:
        contract_type: Optional filter. One of: Employment Contract, Lease Agreement,
                      NDA, SaaS Agreement, Construction Contract, Supply Agreement,
                      Professional Services Agreement, Commercial Agency Agreement,
                      Shareholder Agreement, Franchise Agreement, Cloud Storage Agreement
        risk_level: Optional filter. One of: critical, high, medium, low
        category: Optional filter. One of: Employment & Labor, Saudization, Termination,
                 Liability, Data Protection & Privacy, Jurisdiction & Dispute Resolution,
                 Governing Law, Payment Terms, Confidentiality, Intellectual Property,
                 Force Majeure, Warranties, Indemnification, Corporate Governance
    """
    return find_risks(contract_type, risk_level, category)


if __name__ == "__main__":
    mcp.run()
