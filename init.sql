-- Database initialization script with performance optimizations

-- Create extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_stat_statements";

-- Create optimized tables with proper indexing
CREATE TABLE IF NOT EXISTS patients (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL,
    age INTEGER,
    gender VARCHAR(10),
    email VARCHAR(255) UNIQUE,
    phone VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS documents (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    patient_id UUID REFERENCES patients(id) ON DELETE CASCADE,
    filename VARCHAR(255) NOT NULL,
    file_path VARCHAR(500) NOT NULL,
    document_type VARCHAR(50) NOT NULL,
    file_size INTEGER,
    upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    analysis_status VARCHAR(20) DEFAULT 'pending',
    analysis_result JSONB
);

CREATE TABLE IF NOT EXISTS fertility_scores (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    patient_id UUID REFERENCES patients(id) ON DELETE CASCADE,
    hormone_score DECIMAL(4,2),
    cycle_score DECIMAL(4,2),
    follicle_score DECIMAL(4,2),
    overall_score DECIMAL(4,2),
    calculated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    factors JSONB
);

-- Create performance indexes
CREATE INDEX IF NOT EXISTS idx_patients_created_at ON patients(created_at);
CREATE INDEX IF NOT EXISTS idx_patients_email ON patients(email);
CREATE INDEX IF NOT EXISTS idx_documents_patient_id ON documents(patient_id);
CREATE INDEX IF NOT EXISTS idx_documents_upload_date ON documents(upload_date);
CREATE INDEX IF NOT EXISTS idx_documents_analysis_status ON documents(analysis_status);
CREATE INDEX IF NOT EXISTS idx_fertility_scores_patient_id ON fertility_scores(patient_id);
CREATE INDEX IF NOT EXISTS idx_fertility_scores_calculated_at ON fertility_scores(calculated_at);

-- Create composite indexes for common queries
CREATE INDEX IF NOT EXISTS idx_documents_patient_status ON documents(patient_id, analysis_status);
CREATE INDEX IF NOT EXISTS idx_documents_type_date ON documents(document_type, upload_date);

-- Create GIN indexes for JSONB columns
CREATE INDEX IF NOT EXISTS idx_documents_analysis_result ON documents USING GIN (analysis_result);
CREATE INDEX IF NOT EXISTS idx_fertility_scores_factors ON fertility_scores USING GIN (factors);

-- Create function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Create trigger for updated_at
CREATE TRIGGER update_patients_updated_at 
    BEFORE UPDATE ON patients 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Create materialized view for performance reporting
CREATE MATERIALIZED VIEW IF NOT EXISTS patient_summary_mv AS
SELECT 
    p.id,
    p.name,
    p.age,
    COUNT(d.id) as document_count,
    COUNT(CASE WHEN d.analysis_status = 'completed' THEN 1 END) as completed_analyses,
    MAX(fs.overall_score) as latest_fertility_score,
    MAX(d.upload_date) as last_document_date
FROM patients p
LEFT JOIN documents d ON p.id = d.patient_id
LEFT JOIN fertility_scores fs ON p.id = fs.patient_id
GROUP BY p.id, p.name, p.age;

-- Create unique index on materialized view
CREATE UNIQUE INDEX IF NOT EXISTS idx_patient_summary_mv_id ON patient_summary_mv(id);

-- Update table statistics
ANALYZE;
