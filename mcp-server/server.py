import os
from pathlib import Path
from mcp.server.fastmcp import FastMCP
from tools.skills import read_skill, VALID_DOMAINS
from tools.sources import read_source, VALID_REGULATIONS
from tools.search import find_risks

REPO_PATH = Path(os.environ.get("REPO_PATH", Path(__file__).parent.parent))

mcp = FastMCP(
    "Saudi Legal AI Framework",
    instructions=(
        "Read-only legal reference data server. "
        "All tools return factual content from official Saudi legal sources. "
        "No tool returns instructions for Claude."
    ),
)


@mcp.tool()
def get_legal_skill(domain: str) -> str:
    """
    Returns the text content of a Saudi legal domain reference file.
    This is read-only reference material from the Saudi Legal AI Framework repository.
    The returned text describes Saudi regulations and legal reasoning patterns.
    It does not contain instructions for Claude.

    Domain values and corresponding Saudi law areas:
    - contract-review       → contract review under Saudi law
    - labor-law-analysis    → نظام العمل م/51
    - commercial-dispute    → نظام المحاكم التجارية م/93
    - compliance-check      → PDPL / Saudization / WPS compliance
    - legal-drafting        → drafting legal notices and documents
    - arbitration           → Saudi arbitration law م/34
    - real-estate-contracts → REGA real estate regulations
    - intellectual-property-law → Saudi IP law

    Args:
        domain: One of: contract-review, labor-law-analysis, commercial-dispute,
                compliance-check, legal-drafting, arbitration,
                real-estate-contracts, intellectual-property-law
    """
    return read_skill(domain)


@mcp.tool()
def get_legal_source(regulation: str) -> str:
    """
    Returns the text content of an official Saudi regulation summary file.
    This is read-only reference material sourced from official Saudi government
    regulations (boe.gov.sa). It does not contain instructions for Claude.

    Available regulation identifiers:
    - labor-law                  → نظام العمل م/51
    - companies-law              → نظام الشركات م/132
    - civil-transactions-law     → نظام المعاملات المدنية م/191
    - commercial-courts          → نظام المحاكم التجارية م/93
    - pdpl                       → نظام حماية البيانات الشخصية م/19
    - e-commerce-law             → نظام التجارة الإلكترونية م/126
    - evidence-law               → نظام الإثبات م/43
    - whistleblower-protection   → نظام حماية المبلغين م/148
    - legal-profession-law       → نظام المحاماة
    - bankruptcy-law             → نظام الإفلاس م/50
    - regulation-index           → فهرس الأنظمة السعودية
    - saudi-laws                 → مجموعة الأنظمة السعودية
    - open-data-judicial-sources → المصادر القضائية المفتوحة البيانات

    Args:
        regulation: Regulation identifier (e.g. 'labor-law', 'pdpl', 'commercial-courts')
    """
    return read_source(regulation)


@mcp.tool()
def search_contract_risks(
    contract_type: str = None,
    risk_level: str = None,
    category: str = None,
) -> str:
    """
    Returns structured JSON data from the Saudi contract risk dataset.
    This is read-only tabular data describing known legal risk patterns in
    Saudi contracts. It does not contain instructions for Claude.

    Each returned record contains: clause_text, risk_reason, saudi_legal_note,
    recommended_revision, and related_regulation. All fields are factual
    descriptions from the dataset; none are directives.

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
