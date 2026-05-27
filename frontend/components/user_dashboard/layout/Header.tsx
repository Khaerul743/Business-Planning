import { Bell, ChevronLeft, Menu, Search, User } from 'lucide-react';
import { usePathname } from 'next/navigation';
import React, { useEffect, useState } from 'react';

interface HeaderProps {
  isSidebarCollapsed: boolean;
  toggleSidebar: () => void;
}

export const Header: React.FC<HeaderProps> = ({
  isSidebarCollapsed,
  toggleSidebar
}) => {
  const pathname = usePathname();
  const [userName, setUserName] = useState<string>('Loading...');
  const [userRole, setUserRole] = useState<string>('');

  useEffect(() => {
    const fetchUser = async () => {
      try {
        const res = await fetch('/api/user');
        if (res.ok) {
          const data = await res.json();
          if (data.status === 'success' && data.data) {
            setUserName(data.data.name);
            setUserRole(data.data.role || 'User');
          }
        }
      } catch (error) {
        console.error("Failed to fetch user data:", error);
        setUserName('User');
      }
    };

    fetchUser();
  }, []);

  // Basic title logic based on route
  const getPageTitle = (path: string) => {
    if (path === '/') return 'Dashboard';
    const segment = path.split('/')[1];
    return segment ? segment.charAt(0).toUpperCase() + segment.slice(1) : 'Page';
  };

  return (
    <header className={`
      sticky top-0 z-30 h-16 
      bg-white/80 backdrop-blur-md border-b border-gray-200
      transition-all duration-300 ease-in-out
      flex items-center justify-between px-6
    `}>
      <div className="flex items-center gap-4">
        <button
          onClick={toggleSidebar}
          className="p-2 rounded-lg hover:bg-gray-100 text-gray-600 focus:outline-none focus:ring-2 focus:ring-indigo-500"
          aria-label="Toggle Sidebar"
        >
          {isSidebarCollapsed ? <Menu size={20} /> : <ChevronLeft size={20} />}
        </button>

        <h1 className="text-xl font-semibold text-gray-800">
          {getPageTitle(pathname)}
        </h1>
      </div>

      <div className="flex items-center gap-4">
        {/* Search Bar - Hidden on small screens */}
        <div className="hidden md:flex items-center relative">
          <Search size={16} className="absolute left-3 text-gray-400" />
          <input
            type="text"
            placeholder="Search..."
            className="pl-9 pr-4 py-1.5 rounded-full border border-gray-200 text-sm focus:outline-none focus:border-indigo-400 focus:ring-1 focus:ring-indigo-400 w-64 transition-all"
          />
        </div>

        {/* Notification Bell */}
        <button className="relative p-2 rounded-full hover:bg-gray-100 text-gray-600">
          <Bell size={20} />
          <span className="absolute top-1.5 right-1.5 w-2 h-2 bg-red-500 rounded-full border-2 border-white"></span>
        </button>

        {/* User Profile */}
        <div className="flex items-center gap-3 pl-2 border-l border-gray-200">
          <div className="text-right hidden sm:block">
            <p className="text-sm font-medium text-gray-900">{userName}</p>
            <p className="text-xs text-gray-500 capitalize">{userRole}</p>
          </div>
          <button className="w-9 h-9 rounded-full bg-indigo-100 flex items-center justify-center text-indigo-700 hover:ring-2 hover:ring-offset-2 hover:ring-indigo-400 transition-all">
            <User size={18} />
          </button>
        </div>
      </div>
    </header>
  );
};
