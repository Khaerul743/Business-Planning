import React from 'react';
import Image from 'next/image';

interface AuthCardProps {
  children: React.ReactNode;
  title: string;
  subtitle: string;
}

export const AuthCard: React.FC<AuthCardProps> = ({ children, title, subtitle }) => {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full space-y-8 bg-white p-8 sm:p-10 rounded-2xl shadow-sm border border-gray-100">
        <div className="flex flex-col items-center">
          <div className="flex items-center justify-center mb-4 transition-transform duration-500 hover:scale-105 cursor-pointer">
             <div className="p-3 bg-indigo-50 rounded-2xl shadow-sm">
               <Image src="/Logo.png" alt="Nusara Logo" width={64} height={64} className="object-contain" />
             </div>
          </div>
          <h2 className="mt-2 text-center text-3xl font-extrabold text-gray-900 tracking-tight">
            {title}
          </h2>
          <p className="mt-3 text-center text-sm text-gray-500 max-w-sm">
            {subtitle}
          </p>
        </div>
        {children}
      </div>
    </div>
  );
};
