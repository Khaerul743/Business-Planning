export interface TokenUsageTrendResponse{
    date: string,
    token: number
}

export interface MessageUsageTrendResponse{
    date: string,
    total_message: number
}

export interface MessageTrendHumanVsAiResponse{
    date: string,
    human: number,
    ai: number
}

export interface CategoryPercentageSample {
    category_type: string;
    sample_messages: string[];
}

export interface CategoryPercentageSummary {
    category_type: string;
    total: number;
    change: string;
}

export interface CategoryPercentageResponse {
    summary: CategoryPercentageSummary[];
    samples: CategoryPercentageSample[];
}

export interface AnalyticInsightResponse {
    id: string;
    created_at: string;
    overview: string;
    insight: string;
    reason: string;
    impact: string;
    recommendation: string;
}

export interface KnowledgeGapResponse {
    id: string;
    created_at: string;
    business_id: string;
    insight: string;
    knowladge_business_gap: string;
    recommendation: string;
}

export interface SentimentSamples {
    positif: string;
    netral: string;
    negatif: string;
}

export interface SentimentAnalysisResponse {
    positif: number;
    netral: number;
    negatif: number;
    total: number;
    samples: SentimentSamples;
}