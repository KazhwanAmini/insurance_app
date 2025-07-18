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
    alert('اطلاعات با موفقیت ذخیره شد.')
  }

  if (!company) return <p>در حال بارگذاری...</p>

  return (
    <div className="profile-container">
      <h2>پروفایل شرکت</h2>
      <form onSubmit={handleSubmit}>
        <label>نام شرکت</label>
        <input name="name" value={company.name} onChange={handleChange} />

        <label>آدرس</label>
        <input name="address" value={company.address} onChange={handleChange} />

        <label>شماره تلفن</label>
        <input name="phone_number" value={company.phone_number} onChange={handleChange} />

        <button type="submit">ذخیره</button>
      </form>

      <div className="credit-box">
        <h3>اعتبار باقی مانده: {company.sms_credit} واحد</h3>
      </div>

      <h3>گزارش پیامک‌ها</h3>
      <table>
        <thead>
          <tr>
            <th>گیرنده</th>
            <th>متن پیام</th>
            <th>تاریخ</th>
          </tr>
        </thead>
        <tbody>
          {logs.map(log => (
            <tr key={log.id}>
              <td>{log.recipient}</td>
              <td>{log.message}</td>
              <td>{new Date(log.sent_at).toLocaleString()}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}

export default CompanyProfilePage
