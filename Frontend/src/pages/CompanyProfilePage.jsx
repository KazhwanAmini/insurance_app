import React, { useEffect, useState } from 'react'
import api from '../api'
import './CompanyProfilePage.css'

const CompanyProfilePage = () => {
  const [company, setCompany] = useState(null)
  const [logs, setLogs] = useState([])

  useEffect(() => {
    api.get('/company/profile/').then(res => setCompany(res.data))
    api.get('/company/sms-logs/').then(res => setLogs(res.data))
  }, [])

  const handleChange = (e) => {
    setCompany({ ...company, [e.target.name]: e.target.value })
  }

  const handleSubmit = (e) => {
    e.preventDefault()
    api.put('/company/profile/', company).then(res => setCompany(res.data))
    alert('✅ اطلاعات با موفقیت ذخیره شد.')
  }

  if (!company) return <div className="loading">در حال بارگذاری اطلاعات...</div>

  return (
    <div className="company-profile-container">
      <div className="profile-header">
        <h2>🧾 پروفایل شرکت</h2>
      </div>

      <form className="company-form" onSubmit={handleSubmit}>
        <div className="form-group">
          <label>نام شرکت</label>
          <input name="name" value={company.name} onChange={handleChange} />
        </div>

        <div className="form-group">
          <label>آدرس</label>
          <input name="address" value={company.address} onChange={handleChange} />
        </div>

        <div className="form-group">
          <label>شماره تلفن</label>
          <input name="phone_number" value={company.phone_number} onChange={handleChange} />
        </div>

        <div className="credit-box-with-button">
          <div className="credit-box">
            <strong>اعتبار پیامک باقی‌مانده:</strong> {company.sms_credit.toLocaleString()} تومان
          </div>
          <a href="/credit-topup" className="topup-btn">افزایش اعتبار</a>
        </div>


        <button type="submit" className="save-button">💾 ذخیره تغییرات</button>
      </form>

    </div>
  )
}

export default CompanyProfilePage
