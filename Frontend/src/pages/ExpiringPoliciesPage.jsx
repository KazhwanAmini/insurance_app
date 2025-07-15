import React from 'react';
import { useQuery } from '@tanstack/react-query';
import api from '../api';
import './ExpiringPoliciesPage.css';
import persian from 'react-date-object/calendars/persian';
import { DateObject } from 'react-multi-date-picker';
import { useTranslation } from 'react-i18next'

export default function ExpiringPoliciesPage() {
  const { t } = useTranslation()

  const { data = [], isLoading, error } = useQuery({
    queryKey: ['expiringPolicies'],
    queryFn: async () => {
      const res = await api.get('expiring-policies/');
      return res.data;
    },
  });

  const sendSMS = async (policy) => {
    const message = prompt(
      `پیام برای ${policy.customer_name}:`,
      `${policy.customer_name} عزیز، بیمه‌نامه ${policy.policy_type} شما از شرکت ${policy.company_name} در تاریخ ${policy.end_date} منقضی می‌شود. لطفا برای تمدید اقدام کنید.`
    );
    if (!message) return;

    try {
      await api.post(`/send-sms/${policy.id}/`, { message });
      alert('پیامک با موفقیت ارسال شد!');
    } catch {
      alert('ارسال پیامک با خطا مواجه شد.');
    }
  };

  const bulkSendSMS = async (days) => {
    if (!window.confirm(`آیا مطمئن هستید که می‌خواهید به مشتریان با بیمه‌نامه منقضی در ${days} روز آینده پیامک ارسال کنید؟`)) return;
    try {
      const res = await api.post(`/send-expiry-sms/${days}/`);
      alert(`پیامک به ${res.data.count} مشتری ارسال شد.`);
    } catch {
      alert('ارسال پیامک گروهی با خطا مواجه شد.');
    }
  };

  if (isLoading) return <p className="loading">در حال بارگذاری...</p>;
  if (error) return <p className="error">خطا در بارگذاری اطلاعات.</p>;
  if (!data.length) return <p className="empty">هیچ بیمه‌نامه‌ای در ۱۰ روز آینده منقضی نمی‌شود.</p>;

  return (
    <div className="expiring-container">
      <h2 className="page-title">📅 بیمه‌نامه‌های در حال انقضا (۱۰ روز آینده)</h2>

      <div className="button-group">
        <button onClick={() => bulkSendSMS(10)}>ارسال پیامک انقضا در ۱۰ روز</button>
        <button onClick={() => bulkSendSMS(5)}>ارسال پیامک انقضا در ۵ روز</button>
        <button onClick={() => bulkSendSMS(1)}>ارسال پیامک انقضا فردا</button>
      </div>

      <table className="expiring-table" dir="rtl">
        <thead>
          <tr>
            <th>نام مشتری</th>
            <th>شماره تلفن</th>
            <th>نوع بیمه</th>
            <th>تاریخ انقضا</th>
            <th>ارسال پیامک</th>
          </tr>
        </thead>
        <tbody>
          {data.map((p) => (
            <tr key={p.id}>
              <td>{p.customer_name}</td>
              <td>{p.customer_phone}</td>
              <td>{t(p.policy_type)}</td>              
              <td>{p.end_date ? new DateObject(p.end_date).convert(persian).format("YYYY/MM/DD") : '-'}</td>
              <td>
                <button className="sms-btn" onClick={() => sendSMS(p)}>
                  📩 ارسال
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
