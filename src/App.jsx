import { Heart, Activity, TrendingUp, Circle, Shield, Users, Lock, Zap } from 'lucide-react'

const styles = `
  * {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
  }

  body {
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    background: #ffffff;
    color: #1a1a1a;
    line-height: 1.6;
  }

  .page-wrapper {
    background: #ffffff;
    min-height: 100vh;
  }

  .main-container {
    background: #ffffff;
    overflow: hidden;
    max-width: 1400px;
    margin: 0 auto;
  }

  /* Navigation */
  .nav {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 16px 40px;
    border-bottom: 1px solid #f0f0f0;
  }

  .logo {
    display: flex;
    align-items: center;
    gap: 10px;
    font-weight: 600;
    font-size: 18px;
    color: #1a1a1a;
  }

  .logo-icon {
    color: #e53e3e;
  }

  .nav-buttons {
    display: flex;
    gap: 8px;
    align-items: center;
  }

  .btn {
    padding: 10px 20px;
    border-radius: 8px;
    font-size: 14px;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s ease;
    border: none;
    font-family: inherit;
  }

  .btn-primary {
    background: #1a1a1a;
    color: white;
  }

  .btn-primary:hover {
    background: #333;
  }

  .btn-secondary {
    background: transparent;
    color: #1a1a1a;
    border: 1px solid #e0e0e0;
  }

  .btn-secondary:hover {
    background: #f5f5f5;
  }

  .btn-ghost {
    background: transparent;
    color: #666;
  }

  .btn-ghost:hover {
    color: #1a1a1a;
  }

  /* Hero Section */
  .hero {
    text-align: center;
    padding: 80px 40px 60px;
  }

  .badge {
    display: inline-block;
    background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%);
    color: #dc2626;
    padding: 8px 20px;
    border-radius: 50px;
    font-size: 13px;
    font-weight: 600;
    margin-bottom: 24px;
  }

  .hero h1 {
    font-size: 48px;
    font-weight: 700;
    line-height: 1.15;
    margin-bottom: 20px;
    max-width: 900px;
    margin-left: auto;
    margin-right: auto;
    color: #0f0f0f;
  }

  .hero p {
    font-size: 17px;
    color: #666;
    max-width: 700px;
    margin: 0 auto 32px;
    line-height: 1.7;
  }

  .hero-buttons {
    display: flex;
    gap: 12px;
    justify-content: center;
    margin-bottom: 60px;
  }

  .stats {
    display: flex;
    justify-content: center;
    gap: 180px;
  }

  .stat {
    text-align: center;
  }

  .stat-value {
    font-size: 36px;
    font-weight: 700;
    color: #1a1a1a;
  }

  .stat-label {
    font-size: 14px;
    color: #888;
    margin-top: 4px;
  }

  /* How It Works */
  .how-it-works {
    padding: 60px 40px 80px;
    text-align: center;
  }

  .section-title {
    font-size: 32px;
    font-weight: 700;
    margin-bottom: 12px;
    color: #0f0f0f;
  }

  .section-subtitle {
    font-size: 16px;
    color: #666;
    margin-bottom: 48px;
  }

  .steps {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 24px;
    max-width: 900px;
    margin: 0 auto;
  }

  .step-card {
    background: #fff;
    border: 1px solid #eaeaea;
    border-radius: 16px;
    padding: 40px 28px;
    text-align: center;
    transition: all 0.2s ease;
  }

  .step-card:hover {
    border-color: #d0d0d0;
    box-shadow: 0 4px 20px rgba(0,0,0,0.06);
  }

  .step-icon {
    width: 56px;
    height: 56px;
    border-radius: 14px;
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 0 auto 20px;
  }

  .step-icon.blue {
    background: #eff6ff;
    color: #3b82f6;
  }

  .step-icon.purple {
    background: #f5f3ff;
    color: #8b5cf6;
  }

  .step-icon.green {
    background: #ecfdf5;
    color: #10b981;
  }

  .step-card h3 {
    font-size: 17px;
    font-weight: 600;
    margin-bottom: 12px;
    color: #1a1a1a;
  }

  .step-card p {
    font-size: 14px;
    color: #666;
    line-height: 1.6;
  }

  /* Why Choose */
  .why-choose {
    padding: 60px 40px 80px;
    text-align: center;
  }

  .features {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 32px 80px;
    max-width: 800px;
    margin: 0 auto;
    text-align: left;
  }

  .feature {
    display: flex;
    gap: 16px;
  }

  .feature-icon {
    width: 40px;
    height: 40px;
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
  }

  .feature-icon.red {
    background: #fef2f2;
    color: #ef4444;
  }

  .feature-icon.blue {
    background: #eff6ff;
    color: #3b82f6;
  }

  .feature-icon.cyan {
    background: #ecfeff;
    color: #06b6d4;
  }

  .feature-icon.pink {
    background: #fdf2f8;
    color: #ec4899;
  }

  .feature h4 {
    font-size: 16px;
    font-weight: 600;
    margin-bottom: 6px;
    color: #1a1a1a;
  }

  .feature p {
    font-size: 14px;
    color: #666;
    line-height: 1.5;
  }

  /* CTA Section */
  .cta {
    background: linear-gradient(135deg, #ef4444 0%, #7c3aed 50%, #3b82f6 100%);
    margin: 0 24px 24px;
    border-radius: 24px;
    padding: 64px 40px;
    text-align: center;
  }

  .cta h2 {
    font-size: 32px;
    font-weight: 700;
    color: white;
    margin-bottom: 12px;
  }

  .cta p {
    font-size: 16px;
    color: rgba(255,255,255,0.9);
    margin-bottom: 28px;
  }

  .btn-cta {
    background: white;
    color: #1a1a1a;
    padding: 14px 32px;
    font-size: 15px;
    font-weight: 600;
    border-radius: 10px;
    border: none;
    cursor: pointer;
    transition: all 0.2s ease;
    font-family: inherit;
  }

  .btn-cta:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 24px rgba(0,0,0,0.2);
  }

  /* Footer */
  .footer {
    background: #1a1a2e;
    padding: 40px;
    text-align: center;
  }

  .footer-logo {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 10px;
    font-weight: 600;
    font-size: 18px;
    color: white;
    margin-bottom: 8px;
  }

  .footer-logo svg {
    color: #ef4444;
  }

  .footer-tagline {
    font-size: 14px;
    color: #9ca3af;
    margin-bottom: 16px;
  }

  .footer-disclaimer {
    font-size: 12px;
    color: #6b7280;
  }

  /* Responsive */
  @media (max-width: 768px) {
    .nav {
      padding: 16px 20px;
    }

    .hero {
      padding: 60px 20px 40px;
    }

    .hero h1 {
      font-size: 32px;
    }

    .stats {
      gap: 60px;
    }

    .steps {
      grid-template-columns: 1fr;
    }

    .features {
      grid-template-columns: 1fr;
      gap: 24px;
    }

    .cta {
      margin: 0 12px 12px;
      padding: 48px 24px;
    }

    .cta h2 {
      font-size: 24px;
    }
  }
`

function App() {
  return (
    <>
      <style>{styles}</style>
      <div className="page-wrapper">
        <div className="main-container">
          {/* Navigation */}
          <nav className="nav">
            <div className="logo">
              <Heart size={22} className="logo-icon" fill="#e53e3e" />
              <span>CardioGuard Assistant</span>
            </div>
            <div className="nav-buttons">
              <button className="btn btn-primary">Get Started</button>
              <button className="btn btn-ghost">Login</button>
              <button className="btn btn-secondary">Sign Up</button>
            </div>
          </nav>

          {/* Hero Section */}
          <section className="hero">
            <div className="badge">Machine-Based Heart Attack Risk Assessment</div>
            <h1>Understand Your Heart Attack Risk with an Advanced Machine Analysis</h1>
            <p>
              Our machine-based system reviews your health information and provides a clear, 
              data-driven estimate of your heart attack risk — fast, simple, and easy to understand.
            </p>
            <div className="hero-buttons">
              <button className="btn btn-primary">Start Free Assessment</button>
              <button className="btn btn-secondary">Learn More</button>
            </div>
            <div className="stats">
              <div className="stat">
                <div className="stat-value">98%</div>
                <div className="stat-label">Prediction Accuracy</div>
              </div>
              <div className="stat">
                <div className="stat-value">24/7</div>
                <div className="stat-label">Available Anytime</div>
              </div>
            </div>
          </section>

          {/* How It Works */}
          <section className="how-it-works">
            <h2 className="section-title">How It Works</h2>
            <p className="section-subtitle">Simple, fast, and accurate health risk assessment</p>
            <div className="steps">
              <div className="step-card">
                <div className="step-icon blue">
                  <Activity size={24} />
                </div>
                <h3>Enter Health Data</h3>
                <p>Input your health parameters including systolic blood pressure, diastolic blood pressure and blood sugar.</p>
              </div>
              <div className="step-card">
                <div className="step-icon purple">
                  <TrendingUp size={24} />
                </div>
                <h3>Machine Analysis</h3>
                <p>Our machine system processes your inputs and calculates your heart attack risk using validated medical data.</p>
              </div>
              <div className="step-card">
                <div className="step-icon green">
                  <Circle size={24} />
                </div>
                <h3>View Your Risk Score</h3>
                <p>See a clear breakdown of your risk level in just a few seconds.</p>
              </div>
            </div>
          </section>

          {/* Why Choose */}
          <section className="why-choose">
            <h2 className="section-title">Why Choose CardioGuard Assistant</h2>
            <p className="section-subtitle">Advanced technology meets healthcare expertise</p>
            <div className="features">
              <div className="feature">
                <div className="feature-icon red">
                  <Shield size={20} />
                </div>
                <div>
                  <h4>Clinically Validated</h4>
                  <p>Our model is trained on extensive medical datasets and validated by healthcare professionals</p>
                </div>
              </div>
              <div className="feature">
                <div className="feature-icon blue">
                  <Users size={20} />
                </div>
                <div>
                  <h4>Trusted by Thousands</h4>
                  <p>Join thousands of users who trust CardioGuard AI for their health monitoring</p>
                </div>
              </div>
              <div className="feature">
                <div className="feature-icon cyan">
                  <Lock size={20} />
                </div>
                <div>
                  <h4>Privacy Protected</h4>
                  <p>Your health data is encrypted and never shared with third parties</p>
                </div>
              </div>
              <div className="feature">
                <div className="feature-icon pink">
                  <Zap size={20} />
                </div>
                <div>
                  <h4>Fast & Simple</h4>
                  <p>Get your risk score in minutes.</p>
                </div>
              </div>
            </div>
          </section>

          {/* CTA Section */}
          <section className="cta">
            <h2>Ready to Take Control of Your Heart Health?</h2>
            <p>Get your personalized risk assessment in just 5 minutes</p>
            <button className="btn-cta">Calculate My Risk Now</button>
          </section>

          {/* Footer */}
          <footer className="footer">
            <div className="footer-logo">
              <Heart size={20} fill="#ef4444" />
              <span>CardioGuard Assistant</span>
            </div>
            <p className="footer-tagline">Advanced machine-driven heart attack risk prediction</p>
            <p className="footer-disclaimer">© 2025 CardioGuard AI. For educational purposes only. Not a substitute for professional medical advice.</p>
          </footer>
        </div>
      </div>
    </>
  )
}

export default App

