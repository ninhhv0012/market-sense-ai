import { useState } from 'react';
import { useMutation, useQuery, gql } from '@apollo/client';

// 1. Định nghĩa GraphQL Queries
const CREATE_ANALYSIS = gql`
  mutation CreateAnalysis($url: String!) {
    createAnalysis(url: $url) {
      analysisRequest {
        id
        status
      }
    }
  }
`;

const GET_ANALYSIS = gql`
  query GetAnalysis($id: UUID!) {
    analysisRequest(id: $id) {
      id
      status
      result
      url
    }
  }
`;

function App() {
  const [url, setUrl] = useState('');
  const [analysisId, setAnalysisId] = useState<string | null>(null);

  // Hook Mutation
  const [createAnalysis, { loading: creating }] = useMutation(CREATE_ANALYSIS, {
    onCompleted: (data) => {
      setAnalysisId(data.createAnalysis.analysisRequest.id);
    }
  });

  // Hook Query (Polling)
  const { data, loading: polling, stopPolling } = useQuery(GET_ANALYSIS, {
    variables: { id: analysisId },
    skip: !analysisId, // Chỉ chạy khi đã có ID
    pollInterval: 2000, // Hỏi server mỗi 2s (Cơ chế Async UI)
    onCompleted: (data) => {
      // Nếu xong hoặc lỗi thì dừng hỏi
      if (data.analysisRequest.status === 'COMPLETED' || data.analysisRequest.status === 'FAILED') {
        stopPolling();
      }
    }
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (url) createAnalysis({ variables: { url } });
  };

  const req = data?.analysisRequest;

  return (
    <div>
      <h1>🚀 MarketSense AI</h1>
      <p>Nhập URL bài báo công nghệ (Tiếng Anh) để phân tích SWOT</p>

      {/* Input Form */}
      <form onSubmit={handleSubmit}>
        <input 
          type="url" 
          placeholder="https://techcrunch.com/..." 
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          required 
        />
        <button type="submit" disabled={creating || (req && req.status !== 'COMPLETED' && req.status !== 'FAILED')}>
          {creating ? 'Sending...' : 'Analyze Now'}
        </button>
      </form>

      {/* Status Monitor */}
      {req && (
        <div className="card">
          <h3>Analysis Status: <span className={`status-badge status-${req.status}`}>{req.status}</span></h3>
          <p>ID: {req.id}</p>
          {req.status === 'PROCESSING' && <p>🤖 AI is reading the article & extracting insights...</p>}
        </div>
      )}

      {/* Result Display */}
      {req && req.status === 'COMPLETED' && req.result && (
        <div className="card">
          <h2>📊 Analysis Result</h2>
          <p><strong>Summary:</strong> {req.result.summary}</p>
          <p><strong>Sentiment:</strong> {req.result.sentiment}</p>
          
          <div className="swot-grid">
            <div className="swot-box">
              <h4>Strengths</h4>
              <ul>{req.result.swot.strengths.map((item: string, i: number) => <li key={i}>{item}</li>)}</ul>
            </div>
            <div className="swot-box">
              <h4>Weaknesses</h4>
              <ul>{req.result.swot.weaknesses.map((item: string, i: number) => <li key={i}>{item}</li>)}</ul>
            </div>
            <div className="swot-box">
              <h4>Opportunities</h4>
              <ul>{req.result.swot.opportunities.map((item: string, i: number) => <li key={i}>{item}</li>)}</ul>
            </div>
            <div className="swot-box">
              <h4>Threats</h4>
              <ul>{req.result.swot.threats.map((item: string, i: number) => <li key={i}>{item}</li>)}</ul>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;