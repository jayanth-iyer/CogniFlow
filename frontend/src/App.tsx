import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { DashboardLayout } from '@/components/DashboardLayout';
import { LoginPage } from '@/pages/LoginPage';
import { RequireAuth } from '@/components/RequireAuth';
import { DashboardHome } from '@/pages/DashboardHome';
import { DocumentsPage } from '@/pages/DocumentsPage';
import { SellersPage } from '@/pages/SellersPage';
import { ChatInterface } from '@/components/ChatInterface'; // Will implement next


function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<LoginPage />} />

        <Route path="/" element={
          <RequireAuth>
            <DashboardLayout />
          </RequireAuth>
        }>
          <Route index element={<DashboardHome />} />
          <Route path="documents" element={<DocumentsPage />} />
          <Route path="sellers" element={<SellersPage />} />
          <Route path="chat" element={<div className="max-w-3xl mx-auto"><ChatInterface /></div>} />
        </Route>

        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
