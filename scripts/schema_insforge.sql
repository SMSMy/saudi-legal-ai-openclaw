-- ─────────────────────────────────────────────────────────────────────────────
-- Saudi Legal AI Framework — InsForge Mirror Schema
-- Phase 1: Minimal Safe Mirror
--
-- REVIEW BEFORE EXECUTION. Do not run this file without reading every statement.
-- Run via InsForge MCP tool (run-raw-sql) or the InsForge SQL editor.
--
-- The CSV at datasets/saudi-contract-risk-dataset.csv is the source of truth.
-- This schema creates a read-only derived mirror — no data lives here exclusively.
--
-- After execution, run scripts/sync_to_insforge.py to load the first data.
-- ─────────────────────────────────────────────────────────────────────────────

BEGIN;

-- ─────────────────────────────────────────────────────────────────────────────
-- Section 1: Enum Types
--
-- Values are copied verbatim from datasets/enums/*.md and mirror the sets in
-- scripts/validate_dataset.py. Do not add or change a value here without first
-- updating the corresponding enum .md file and validate_dataset.py (see the
-- Phase 5 enum evolution protocol in the implementation plan).
-- ─────────────────────────────────────────────────────────────────────────────

CREATE TYPE risk_level_t AS ENUM (
    'critical',
    'high',
    'medium',
    'low'
);

-- Hyphens are intentional: 'pending-review' and 'community-reviewed' match
-- datasets/enums/verification-status.md exactly.
CREATE TYPE verification_status_t AS ENUM (
    'draft',
    'pending-review',
    'community-reviewed',
    'reviewed',
    'verified',
    'deprecated',
    'superseded'
);

CREATE TYPE contract_type_t AS ENUM (
    'Employment Contract',
    'SaaS Agreement',
    'Professional Services Agreement',
    'Construction Contract',
    'Supply Agreement',
    'NDA',
    'Shareholder Agreement',
    'Franchise Agreement',
    'Commercial Agency Agreement',
    'Lease Agreement',
    'Cloud Storage Agreement'
);

CREATE TYPE clause_category_t AS ENUM (
    'Jurisdiction & Dispute Resolution',
    'Liability',
    'Data Protection & Privacy',
    'Intellectual Property',
    'Termination',
    'Confidentiality',
    'Payment Terms',
    'Governing Law',
    'Force Majeure',
    'Warranties',
    'Indemnification',
    'Employment & Labor',
    'Saudization',
    'Corporate Governance'
);

CREATE TYPE industry_t AS ENUM (
    'Technology',
    'Professional Services',
    'Construction',
    'Healthcare',
    'Real Estate',
    'Finance',
    'Retail',
    'Logistics',
    'Energy',
    'Education',
    'Government',
    'General'
);

CREATE TYPE language_code_t AS ENUM (
    'en',
    'ar',
    'bilingual'
);

CREATE TYPE source_type_t AS ENUM (
    'hypothetical',
    'abstracted',
    'published_case',
    'standard_form'
);


-- ─────────────────────────────────────────────────────────────────────────────
-- Section 2: Tables
-- ─────────────────────────────────────────────────────────────────────────────

CREATE TABLE contract_risk_clauses (

    -- ── CSV columns (16) ──────────────────────────────────────────────────────
    -- Column order and names match datasets/schema.md exactly.
    id                    INTEGER                NOT NULL,
    contract_type         contract_type_t        NOT NULL,
    clause_category       clause_category_t      NOT NULL,
    clause_text           TEXT                   NOT NULL CHECK (length(clause_text) > 0),
    risk_level            risk_level_t           NOT NULL,
    risk_reason           TEXT                   NOT NULL CHECK (length(risk_reason) > 0),
    saudi_legal_note      TEXT                   NOT NULL CHECK (length(saudi_legal_note) > 0),
    recommended_revision  TEXT                   NOT NULL CHECK (length(recommended_revision) > 0),
    related_regulation    TEXT                   NOT NULL,
    requires_escalation   BOOLEAN                NOT NULL,
    language              language_code_t        NOT NULL,
    industry              industry_t             NOT NULL,
    source_type           source_type_t          NOT NULL,
    reviewed_by_lawyer    BOOLEAN                NOT NULL,
    notes                 TEXT,                           -- nullable: optional in CSV
    verification_status   verification_status_t  NOT NULL DEFAULT 'draft',

    -- ── Mirror-only tracking columns (not in CSV) ────────────────────────────
    -- These columns are populated by sync_to_insforge.py on every sync.
    csv_row_hash          TEXT                   NOT NULL, -- SHA-256 of raw CSV row dict
    synced_at             TIMESTAMPTZ            NOT NULL DEFAULT now(),
    git_sha               TEXT                   NOT NULL, -- git commit that produced this sync

    -- ── Constraints ──────────────────────────────────────────────────────────
    CONSTRAINT contract_risk_clauses_pkey
        PRIMARY KEY (id),

    -- Mirrors the rule in datasets/schema.md §16 and datasets/enums/verification-status.md:
    -- "If verification_status = verified then reviewed_by_lawyer must be yes."
    CONSTRAINT verified_requires_lawyer_review
        CHECK (
            verification_status <> 'verified' OR reviewed_by_lawyer = TRUE
        )
);

-- Audit log: one row per sync run. Never modified after insert.
CREATE TABLE contract_risk_sync_log (
    id              SERIAL        PRIMARY KEY,
    synced_at       TIMESTAMPTZ   NOT NULL DEFAULT now(),
    git_sha         TEXT          NOT NULL,
    csv_path        TEXT          NOT NULL DEFAULT 'datasets/saudi-contract-risk-dataset.csv',
    rows_total      INTEGER       NOT NULL,
    rows_inserted   INTEGER       NOT NULL DEFAULT 0,
    rows_updated    INTEGER       NOT NULL DEFAULT 0,
    rows_skipped    INTEGER       NOT NULL DEFAULT 0,
    sync_status     TEXT          NOT NULL
        CHECK (sync_status IN ('success', 'partial', 'failed')),
    error_detail    TEXT                              -- NULL on success
);


-- ─────────────────────────────────────────────────────────────────────────────
-- Section 3: Phase 1 Indexes
--
-- Minimal set for Phase 1: the two most common single-column filters.
-- Composite indexes and the full-text GIN index are deferred to Phase 2.
-- ─────────────────────────────────────────────────────────────────────────────

CREATE INDEX idx_crc_risk_level
    ON contract_risk_clauses (risk_level);

CREATE INDEX idx_crc_verification_status
    ON contract_risk_clauses (verification_status);


-- ─────────────────────────────────────────────────────────────────────────────
-- Section 4: Row-Level Security
--
-- contract_risk_clauses: public SELECT allowed; no write policy = writes are
--   structurally blocked for anon and authenticated roles.
--   Only the service role (used by sync_to_insforge.py) can write.
--
-- contract_risk_sync_log: no public policy at all = fully internal.
--   Only the service role can read or write.
-- ─────────────────────────────────────────────────────────────────────────────

ALTER TABLE contract_risk_clauses  ENABLE ROW LEVEL SECURITY;
ALTER TABLE contract_risk_sync_log ENABLE ROW LEVEL SECURITY;

CREATE POLICY "public_select_clauses"
    ON contract_risk_clauses
    FOR SELECT
    TO anon, authenticated
    USING (true);

COMMIT;


-- ─────────────────────────────────────────────────────────────────────────────
-- ROLLBACK
--
-- To undo everything above, run these statements in order.
-- Dropping a table automatically drops its indexes and policies.
-- Types must be dropped after tables (tables reference the types).
-- Safe at any point: the CSV in git is unchanged and is the source of truth.
--
-- DROP TABLE IF EXISTS contract_risk_sync_log;
-- DROP TABLE IF EXISTS contract_risk_clauses;
-- DROP TYPE  IF EXISTS source_type_t;
-- DROP TYPE  IF EXISTS language_code_t;
-- DROP TYPE  IF EXISTS industry_t;
-- DROP TYPE  IF EXISTS clause_category_t;
-- DROP TYPE  IF EXISTS contract_type_t;
-- DROP TYPE  IF EXISTS verification_status_t;
-- DROP TYPE  IF EXISTS risk_level_t;
-- ─────────────────────────────────────────────────────────────────────────────
