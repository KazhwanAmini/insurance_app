// src/pages/Home.js
import React, { useEffect, useState } from 'react'
import './Home.css'
const Home = () => {
const [companyStatus, setCompanyStatus] = useState(null)

  useEffect(() => {
    const status = localStorage.getItem('company_status')
    setCompanyStatus(status)
  }, [])

  if (companyStatus === 'pending') {
    return (
      <div style={{ padding: '2rem', color: 'orange', textAlign: 'center' }}>
        <h2>شرکت شما در انتظار تایید مدیریت است</h2>
        <p>لطفاً منتظر بمانید تا دسترسی شما فعال شود.</p>
      </div>
    )
  }

  if (companyStatus === 'deactivated') {
    return (
      <div style={{ padding: '2rem', color: 'red', textAlign: 'center' }}>
        <h2>دسترسی شرکت شما غیرفعال شده است</h2>
        <p>برای فعال‌سازی لطفاً با مدیریت تماس بگیرید.</p>
      </div>
    )
  }
  
  return (
    <div className="pro-home-container">
      <div className="pro-home-card">
        <h1>به پورتال مدیریت بیمه نامه ها <span className="highlight">خوش آمدید</span></h1>
        <p className="subtext">
          به راحتی مشتریان و بیمه نامه های خود را در یک مکان مدیریت کنید.
        </p>
       
      </div>
    </div>
  )
}

export default Home
