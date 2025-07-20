import React, { useState } from 'react'
import './TopUpPage.css'
import api from '../api'
import persian from 'react-date-object/calendars/persian'
import DatePicker from "react-multi-date-picker"
import persian_fa from "react-date-object/locales/persian_fa"

const CompanyTopUpPage = () => {
  const [form, setForm] = useState({
    card_last4: '',
    payment_date: null,
    amount: '',
    tracking_code: ''
  })

  const [submitted, setSubmitted] = useState(false)

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value })
  }

  const handleDateChange = (dateObject) => {
    setForm({ ...form, payment_date: dateObject })
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    try {
      await api.post('/credit-topup/', {
        ...form,
        payment_date: form.payment_date?.format("YYYY-MM-DD")  // send Gregorian or formatted string
      })
      setSubmitted(true)
    } catch (err) {
      alert('خطا در ارسال اطلاعات.')
    }
  }

  return (
    <div className="topup-container">
      <h2>افزایش اعتبار</h2>
      <p className="instructions">
        لطفاً مبلغ مورد نظر را به شماره کارت <strong>6037-9918-XXXX-XXXX</strong> واریز کنید، سپس اطلاعات زیر را وارد نمایید.
      </p>

      <form className="topup-form" onSubmit={handleSubmit}>
        <label>۴ رقم آخر کارت شما</label>
        <input name="card_last4" maxLength={4} value={form.card_last4} onChange={handleChange} required />

        <label>تاریخ پرداخت</label>
        <DatePicker
          calendar={persian}
          locale={persian_fa}
          calendarPosition="top-left"
          value={form.payment_date}
          onChange={handleDateChange}
          format="YYYY/MM/DD"
          placeholder="تاریخ را انتخاب کنید"
        />

        <label>مبلغ واریز شده (تومان)</label>
        <input name="amount" type="number" value={form.amount} onChange={handleChange} required />

        <label>کد پیگیری</label>
        <input name="tracking_code" value={form.tracking_code} onChange={handleChange} required />

        <button type="submit" className="submit-btn">ارسال اطلاعات</button>
      </form>

      {submitted && <p className="success-message">درخواست شما با موفقیت ثبت شد و منتظر تایید مدیر است.</p>}
    </div>
  )
}

export default CompanyTopUpPage
