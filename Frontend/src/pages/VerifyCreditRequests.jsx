import React, { useEffect, useState } from 'react'
import api from '../api'
import './TopUpPage.css'

const VerifyCreditRequests = () => {
  const [requests, setRequests] = useState([])

  const fetchRequests = async () => {
    const res = await api.get('/credit-topup/admin/')
    const sorted = res.data.sort((a, b) => a.is_verified - b.is_verified)
    setRequests(sorted)
  }

  useEffect(() => {
    fetchRequests()
  }, [])

  const verifyRequest = async (id) => {
    const amount = prompt("مقدار اعتبار (SMS Credit) را وارد کنید:")
    if (!amount) return
    await api.patch(`credit-topup/verify/${id}/`, { sms_credit: amount })
    fetchRequests()
  }

  return (
    <div className="topup-container">
      <h2>درخواست‌های افزایش اعتبار</h2>
      <table className="sms-log-table">
        <thead>
          <tr>
            <th>نام شرکت</th>
            <th>۴ رقم آخر کارت</th>
            <th>تاریخ پرداخت</th>
            <th>مبلغ</th>
            <th>کد پیگیری</th>
            <th>وضعیت</th>
            <th>عملیات</th>
          </tr>
        </thead>
        <tbody>
          {requests.map(req => (
            <tr key={req.id} className={req.is_verified ? 'verified-row' : ''}>
              <td>{req.company_name}</td>
              <td>{req.card_last4}</td>
              <td>{req.payment_date}</td>
              <td>{req.amount}</td>
              <td>{req.tracking_code}</td>
              <td>
                <span className={`status-badge ${req.is_verified ? 'verified' : 'pending'}`}>
                  {req.is_verified ? 'تأیید شده' : 'در انتظار'}
                </span>
              </td>
              <td>
                <button
                  className={`submit-btn ${req.is_verified ? 'disabled' : ''}`}
                  onClick={() => !req.is_verified && verifyRequest(req.id)}
                  disabled={req.is_verified}
                >
                  {req.is_verified ? 'تأیید شده' : 'تأیید و افزودن اعتبار'}
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}

export default VerifyCreditRequests
