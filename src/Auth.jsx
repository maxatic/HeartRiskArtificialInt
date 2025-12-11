import { useState } from 'react'
import { User, Stethoscope } from 'lucide-react'
import { useNavigate } from 'react-router-dom'

const styles = `
  .auth-container {
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    background: #f8f9fa;
    padding: 20px;
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
  }

  .auth-card {
    background: white;
    border-radius: 24px;
    padding: 40px;
    width: 100%;
    max-width: 440px;
    box-shadow: 0 4px 24px rgba(0, 0, 0, 0.06);
  }

  .tab-toggle {
    display: flex;
    background: #f3f4f6;
    border-radius: 50px;
    padding: 4px;
    margin-bottom: 32px;
  }

  .tab-btn {
    flex: 1;
    padding: 12px 24px;
    border: none;
    background: transparent;
    border-radius: 50px;
    font-size: 15px;
    font-weight: 500;
    color: #6b7280;
    cursor: pointer;
    transition: all 0.2s ease;
    font-family: inherit;
  }

  .tab-btn.active {
    background: white;
    color: #1a1a1a;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  }

  .auth-header {
    text-align: center;
    margin-bottom: 32px;
  }

  .auth-header h1 {
    font-size: 24px;
    font-weight: 700;
    color: #1a1a1a;
    margin-bottom: 8px;
  }

  .auth-header p {
    font-size: 15px;
    color: #6b7280;
  }

  .role-label {
    text-align: center;
    font-size: 15px;
    color: #6b7280;
    margin-bottom: 20px;
  }

  .role-selection {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 16px;
    margin-bottom: 24px;
  }

  .role-card {
    background: white;
    border: 1px solid #e5e7eb;
    border-radius: 16px;
    padding: 28px 20px;
    text-align: center;
    cursor: pointer;
    transition: all 0.2s ease;
  }

  .role-card:hover {
    border-color: #d1d5db;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.06);
  }

  .role-card.selected {
    border-color: #3b82f6;
    background: #f8faff;
  }

  .role-icon {
    width: 56px;
    height: 56px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 0 auto 16px;
  }

  .role-icon.patient {
    background: #eff6ff;
    color: #3b82f6;
  }

  .role-icon.doctor {
    background: #f3e8ff;
    color: #8b5cf6;
  }

  .role-card h3 {
    font-size: 16px;
    font-weight: 600;
    color: #1a1a1a;
    margin-bottom: 6px;
  }

  .role-card p {
    font-size: 13px;
    color: #9ca3af;
    line-height: 1.4;
  }

  .selected-role {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 24px;
    padding: 0 4px;
  }

  .selected-role-info {
    display: flex;
    align-items: center;
    gap: 10px;
    font-size: 14px;
    color: #6b7280;
  }

  .selected-role-info svg {
    color: #9ca3af;
  }

  .change-btn {
    background: none;
    border: none;
    color: #3b82f6;
    font-size: 14px;
    font-weight: 500;
    cursor: pointer;
    font-family: inherit;
  }

  .change-btn:hover {
    text-decoration: underline;
  }

  .form-group {
    margin-bottom: 20px;
  }

  .form-group label {
    display: block;
    font-size: 14px;
    font-weight: 500;
    color: #1a1a1a;
    margin-bottom: 8px;
  }

  .form-group input {
    width: 100%;
    padding: 14px 16px;
    border: 1px solid #e5e7eb;
    border-radius: 12px;
    font-size: 15px;
    color: #1a1a1a;
    background: #f9fafb;
    transition: all 0.2s ease;
    font-family: inherit;
    box-sizing: border-box;
  }

  .form-group input::placeholder {
    color: #9ca3af;
  }

  .form-group input:focus {
    outline: none;
    border-color: #3b82f6;
    background: white;
    box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
  }

  .submit-btn {
    width: 100%;
    padding: 16px;
    background: #1a1a2e;
    color: white;
    border: none;
    border-radius: 12px;
    font-size: 15px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s ease;
    font-family: inherit;
    margin-top: 8px;
  }

  .submit-btn:hover {
    background: #2d2d44;
  }

  .back-link {
    display: block;
    text-align: center;
    margin-top: 24px;
    color: #6b7280;
    font-size: 14px;
    text-decoration: none;
  }

  .back-link:hover {
    color: #3b82f6;
  }
`

function Auth() {
  const navigate = useNavigate()
  const [activeTab, setActiveTab] = useState('signin') // 'signin' or 'signup'
  const [selectedRole, setSelectedRole] = useState(null) // 'patient' or 'doctor'
  const [showForm, setShowForm] = useState(false)

  // Form states
  const [formData, setFormData] = useState({
    fullName: '',
    email: '',
    doctorId: '',
    password: '',
    confirmPassword: ''
  })

  const handleRoleSelect = (role) => {
    setSelectedRole(role)
    setShowForm(true)
  }

  const handleChange = () => {
    setShowForm(false)
    setSelectedRole(null)
  }

  const handleInputChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    })
  }

  const handleSubmit = (e) => {
    e.preventDefault()
    // Handle form submission - just frontend for now
    console.log('Form submitted:', { activeTab, selectedRole, formData })
    alert(`${activeTab === 'signin' ? 'Sign In' : 'Sign Up'} submitted as ${selectedRole}!`)
  }

  const renderRoleSelection = () => (
    <>
      <p className="role-label">I am a:</p>
      <div className="role-selection">
        <div 
          className={`role-card ${selectedRole === 'patient' ? 'selected' : ''}`}
          onClick={() => handleRoleSelect('patient')}
        >
          <div className="role-icon patient">
            <User size={24} />
          </div>
          <h3>Patient</h3>
          <p>Get health assessments</p>
        </div>
        <div 
          className={`role-card ${selectedRole === 'doctor' ? 'selected' : ''}`}
          onClick={() => handleRoleSelect('doctor')}
        >
          <div className="role-icon doctor">
            <Stethoscope size={24} />
          </div>
          <h3>Doctor</h3>
          <p>Manage patient care</p>
        </div>
      </div>
    </>
  )

  const renderSignInForm = () => (
    <form onSubmit={handleSubmit}>
      <div className="selected-role">
        <div className="selected-role-info">
          {selectedRole === 'patient' ? <User size={18} /> : <Stethoscope size={18} />}
          <span>Signing in as {selectedRole === 'patient' ? 'Patient' : 'Doctor'}</span>
        </div>
        <button type="button" className="change-btn" onClick={handleChange}>Change</button>
      </div>

      <div className="form-group">
        <label>Email</label>
        <input
          type="email"
          name="email"
          placeholder="Enter your email"
          value={formData.email}
          onChange={handleInputChange}
          required
        />
      </div>

      <div className="form-group">
        <label>Password</label>
        <input
          type="password"
          name="password"
          placeholder="Enter your password"
          value={formData.password}
          onChange={handleInputChange}
          required
        />
      </div>

      <button type="submit" className="submit-btn">Sign In</button>
    </form>
  )

  const renderSignUpForm = () => (
    <form onSubmit={handleSubmit}>
      <div className="selected-role">
        <div className="selected-role-info">
          {selectedRole === 'patient' ? <User size={18} /> : <Stethoscope size={18} />}
          <span>Signing up as {selectedRole === 'patient' ? 'Patient' : 'Doctor'}</span>
        </div>
        <button type="button" className="change-btn" onClick={handleChange}>Change</button>
      </div>

      <div className="form-group">
        <label>Full Name</label>
        <input
          type="text"
          name="fullName"
          placeholder="Enter your full name"
          value={formData.fullName}
          onChange={handleInputChange}
          required
        />
      </div>

      <div className="form-group">
        <label>Email</label>
        <input
          type="email"
          name="email"
          placeholder="Enter your email"
          value={formData.email}
          onChange={handleInputChange}
          required
        />
      </div>

      {selectedRole === 'patient' && (
        <div className="form-group">
          <label>Doctor ID (optional)</label>
          <input
            type="text"
            name="doctorId"
            placeholder="Enter your license number"
            value={formData.doctorId}
            onChange={handleInputChange}
          />
        </div>
      )}

      <div className="form-group">
        <label>Password</label>
        <input
          type="password"
          name="password"
          placeholder="Create a password"
          value={formData.password}
          onChange={handleInputChange}
          required
        />
      </div>

      <div className="form-group">
        <label>Confirm Password</label>
        <input
          type="password"
          name="confirmPassword"
          placeholder="Confirm your password"
          value={formData.confirmPassword}
          onChange={handleInputChange}
          required
        />
      </div>

      <button type="submit" className="submit-btn">Create Account</button>
    </form>
  )

  return (
    <>
      <style>{styles}</style>
      <div className="auth-container">
        <div className="auth-card">
          {/* Tab Toggle */}
          <div className="tab-toggle">
            <button
              className={`tab-btn ${activeTab === 'signin' ? 'active' : ''}`}
              onClick={() => {
                setActiveTab('signin')
                setShowForm(false)
                setSelectedRole(null)
              }}
            >
              Sign In
            </button>
            <button
              className={`tab-btn ${activeTab === 'signup' ? 'active' : ''}`}
              onClick={() => {
                setActiveTab('signup')
                setShowForm(false)
                setSelectedRole(null)
              }}
            >
              Sign Up
            </button>
          </div>

          {/* Header */}
          <div className="auth-header">
            <h1>{activeTab === 'signin' ? 'Welcome Back' : 'Create Account'}</h1>
            <p>{activeTab === 'signin' ? 'Sign in to your account' : 'Join CardioGuard AI today'}</p>
          </div>

          {/* Content */}
          {!showForm && renderRoleSelection()}
          {showForm && activeTab === 'signin' && renderSignInForm()}
          {showForm && activeTab === 'signup' && renderSignUpForm()}

          {/* Back to Home */}
          <a href="/" className="back-link" onClick={(e) => { e.preventDefault(); navigate('/') }}>
            ← Back to Home
          </a>
        </div>
      </div>
    </>
  )
}

export default Auth

