import React, { useEffect, useState } from 'react'
import api from '../api'
import './CompanySMSLogPage.css'

const CompanySMSLogPage = () => {
  const [logs, setLogs] = useState([])

  useEffect(() => {
    api.get('/company/sms-logs/').then(res => setLogs(res.data))
  }, [])

  return (
    <div className="sms-log-container">
      <h2>گزارش پیامک‌های شرکت</h2>
      <table className="sms-log-table">
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
              <td>{new Date(log.sent_at).toLocaleString('fa-IR')}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}

export default CompanySMSLogPage
