import os
import sys
from pathlib import Path
from mcp.server.fastmcp import FastMCP

from tools.skills import read_skill, VALID_DOMAINS
from tools.sources import read_source, VALID_REGULATIONS
from tools.search import find_risks

REPO_PATH = Path(os.environ.get("REPO_PATH", Path(__file__).parent.parent))

mcp = FastMCP(
    "Saudi Legal AI Framework",
    instructions=(
        "Saudi legal knowledge retrieval server for OpenClaw. "
        "All tools return factual legal context from official Saudi sources "
        "(skills, regulation summaries, contract risk dataset). "
        "The OpenClaw agent performs the legal analysis itself using its active "
        "model — this server never calls an external LLM and needs no API keys. "
        "Always pair retrieval with the framework's disclaimer: analysis is "
        "preliminary and must be reviewed by a licensed Saudi legal professional."
    ),
)


@mcp.tool()
def get_legal_skill(domain: str) -> str:
    """
    Returns the Saudi legal skill/guide for a legal domain. The skill tells the
    agent HOW to reason about that domain under Saudi law (scope, key rules,
    red flags, recommended structure). Content is factual reference only.

    Args:
        domain: One of: contract-review, labor-law-analysis, commercial-dispute,
               compliance-check, legal-drafting, arbitration,
               real-estate-contracts, intellectual-property-law
    """
    return read_skill(domain)


@mcp.tool()
def get_regulation_source(regulation: str) -> str:
    """
    Returns the reference summary of an official Saudi regulation (decree
    numbers, key articles, competent authority, deadlines). Factual reference
    only — not the full legal text.

    Args:
        regulation: One of: labor-law, companies-law, civil-transactions-law,
                   commercial-courts, pdpl, e-commerce-law, evidence-law,
                   whistleblower-protection, legal-profession-law,
                   arbitration-law, bankruptcy-law, sports-law-saff, fifa-rstp,
                   real-estate-arbitration-reac, regulation-index, saudi-laws,
                   open-data-judicial-sources
    """
    return read_source(regulation)


@mcp.tool()
def get_legal_context(contract_type: str) -> str:
    """
    One-call retrieval of everything needed to analyze a contract type under
    Saudi law: the matching skill (reasoning guide), the relevant regulation
    summary, and known risk patterns from the dataset. The agent then performs
    the analysis with its active model.

    Args:
        contract_type: One of: Employment Contract, Lease Agreement,
                      Construction Contract, Supply Agreement, NDA,
                      SaaS Agreement, Cloud Storage Agreement,
                      Professional Services Agreement,
                      Commercial Agency Agreement, Shareholder Agreement,
                      Franchise Agreement
    """
    skill_map = {
        "Employment Contract": "labor-law-analysis",
        "Lease Agreement": "real-estate-contracts",
        "Construction Contract": "commercial-dispute",
        "Supply Agreement": "commercial-dispute",
        "NDA": "compliance-check",
        "SaaS Agreement": "compliance-check",
        "Cloud Storage Agreement": "compliance-check",
        "Professional Services Agreement": "contract-review",
        "Commercial Agency Agreement": "commercial-dispute",
        "Shareholder Agreement": "contract-review",
        "Franchise Agreement": "commercial-dispute",
    }
    source_map = {
        "labor-law-analysis": "labor-law",
        "real-estate-contracts": "real-estate-arbitration-reac",
        "commercial-dispute": "commercial-courts",
        "compliance-check": "pdpl",
        "contract-review": "civil-transactions-law",
    }
    skill_domain = skill_map.get(contract_type)
    if skill_domain is None:
        return (
            f"Unknown contract_type '{contract_type}'. "
            f"Valid types: {', '.join(sorted(skill_map))}"
        )
    skill = read_skill(skill_domain)
    source = read_source(source_map[skill_domain])
    risks = find_risks(contract_type=contract_type)
    return (
        f"## Skill: {skill_domain}\n{skill}\n\n"
        f"## Legal Source\n{source}\n\n"
        f"## Known Risk Patterns for {contract_type}\n{risks}"
    )


@mcp.tool()
def search_contract_risks(
    contract_type: str = None,
    risk_level: str = None,
    category: str = None,
) -> str:
    """
    Returns structured JSON data from the Saudi contract risk dataset.
    Read-only tabular data describing known legal risk patterns in Saudi
    contracts. Each record contains: risk_level, category, clause_text,
    risk_reason, saudi_legal_note, recommended_revision, related_regulation,
    requires_escalation flag.

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


@mcp.tool()
def list_legal_domains() -> str:
    """Lists all available legal skill domains and regulation sources."""
    return (
        "Skills: " + ", ".join(sorted(VALID_DOMAINS)) +
        "\n\nRegulations: " + ", ".join(sorted(VALID_REGULATIONS))
    )


if __name__ == "__main__":
    mcp.run()
