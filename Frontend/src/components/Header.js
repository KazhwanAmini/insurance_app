import React, { useEffect, useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import './Header.css'
import { useTranslation } from 'react-i18next'
import api from '../api'

const Header = () => {
  const { t } = useTranslation()
  const token = localStorage.getItem('access')
  const navigate = useNavigate()
  const [companyName, setCompanyName] = useState('')
  const [companyStatus, setCompanyStatus] = useState(null)
  const [menuOpen, setMenuOpen] = useState(false)

  useEffect(() => {
    setCompanyName(localStorage.getItem('company_name'))
    
    const status = localStorage.getItem('company_status')
    setCompanyStatus(status)

    // const fetchCompany = async () => {
    //   if (token) {
    //     try {
    //       const res = await api.get('/me/')
    //       setCompanyName(res.data.company_name || '')
    //     } catch (err) {
    //       console.error('Failed to fetch company info:', err)
    //     }
    //   }
    // }
    // fetchCompany()
  }, [token])

  const handleLogout = () => {
    localStorage.clear()
    navigate('/login')
  }

  return (
    <header className="pro-header">
      <div className="pro-header-left">
        {token && companyStatus == 'active' && (
          <div className="dropdown">
            <button className="dropdown-toggle" onClick={() => setMenuOpen(!menuOpen)}>
              🏢 {companyName} ▾
            </button>
            {menuOpen && (
              <div className="dropdown-menu">
                <Link to="/" onClick={() => setMenuOpen(false)}>{t('home')}</Link>
                <Link to="/customers" onClick={() => setMenuOpen(false)}>{t('customers')}</Link>
                <Link to="/expiring-policies" onClick={() => setMenuOpen(false)}>{t('expiring_policies')}</Link>
              </div>
            )}
          </div>
        )}
      </div>

      <nav className="pro-nav">
        {!token && <Link to="/register">{t('signup')}</Link>}
        {!token && <Link to="/login">{t('login')}</Link>}
        {token && (
          <button className="logout-btn" onClick={handleLogout}>
            {t('logout')}
          </button>
        )}
      </nav>
    </header>
  )
}

export default Header
