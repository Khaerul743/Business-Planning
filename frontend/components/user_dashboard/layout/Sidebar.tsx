import {
  Bot,
  Briefcase,
  FileText,
  LayoutDashboard,
  LogOut,
  MessageSquare,
  MessageCircle,
  PieChart,
  Lightbulb,
  Play,
  Settings,
  Users
} from 'lucide-react';
import React from 'react';
import Image from 'next/image';
import { Exo_2 } from 'next/font/google';

const exo2 = Exo_2({ subsets: ['latin'], weight: ['600', '700'] });
import { SidebarItem } from './SidebarItem';
import { SidebarSection } from './SidebarSection';
import { redirect } from 'next/dist/server/api-utils';

interface SidebarProps {
  isCollapsed: boolean;
}

export const Sidebar: React.FC<SidebarProps> = ({ isCollapsed }) => {
  async function handleLogout() {
    try {
      const res = await fetch("/api/auth/logout", { method: "POST" });
      const data = await res.json();

      if (!res.ok) {
        alert("Error");
        return;
      }

      alert(data.message);
      // Redirect to /login after successful logout
      window.location.href = "/login";
    } catch (error) {
      console.error(error);
      alert("Error logging out");
    }
  }
  return (
    <aside 
      className={`
        fixed left-0 top-0 bottom-0 z-40
        flex flex-col bg-slate-50 border-r border-gray-200
        transition-all duration-300 ease-in-out
        ${isCollapsed ? 'w-[72px]' : 'w-[240px]'}
      `}
    >
      {/* Logo Area */}
      <div className={`
        h-16 flex items-center border-b border-gray-200
        ${isCollapsed ? 'justify-center px-2' : 'px-6'}
      `}>
        <div className="flex items-center gap-2 font-bold text-xl text-indigo-950">
          <Image 
            src="/Logo.png" 
            alt="Nusara Logo" 
            width={32} 
            height={32} 
            className="object-contain"
          />
          {!isCollapsed && <span className={`tracking-wide transition-opacity duration-300 ${exo2.className}`}>NUSARA</span>}
        </div>
      </div>

      {/* Navigation Content */}
      <div className="flex-1 overflow-y-auto py-4 scrollbar-thin scrollbar-thumb-gray-200">
        
        <SidebarSection title="Main" isCollapsed={isCollapsed}>
          <SidebarItem icon={LayoutDashboard} label="Dashboard" href="/dashboard" isCollapsed={isCollapsed} />
          <SidebarItem icon={MessageSquare} label="Conversations" href="/conversations" isCollapsed={isCollapsed} />
        </SidebarSection>

        <SidebarSection title="Channels" isCollapsed={isCollapsed}>
          <SidebarItem icon={MessageCircle} label="WhatsApp" href="/whatsapp" isCollapsed={isCollapsed} />
        </SidebarSection>

        <SidebarSection title="Agent Control" isCollapsed={isCollapsed}>
          <SidebarItem icon={Bot} label="Agents" href="/agents" isCollapsed={isCollapsed} />
          <SidebarItem icon={Play} label="Playground" href="/playground" isCollapsed={isCollapsed} />
          <SidebarItem icon={Users} label="Customers" href="/customers" isCollapsed={isCollapsed} />
          <SidebarItem icon={Briefcase} label="Business Knowledge" href="/business" isCollapsed={isCollapsed} />
          <SidebarItem icon={FileText} label="Document Knowledge" href="/documents" isCollapsed={isCollapsed} />
        </SidebarSection>

        <SidebarSection title="Intelligence" isCollapsed={isCollapsed}>
          <SidebarItem icon={PieChart} label="Analytics" href="/analytics" isCollapsed={isCollapsed} />
          <SidebarItem icon={Lightbulb} label="Insight" href="/insight" isCollapsed={isCollapsed} />
        </SidebarSection>
        
        <SidebarSection title="System" isCollapsed={isCollapsed}>
          <SidebarItem icon={Settings} label="Settings" href="/setting" isCollapsed={isCollapsed} />
        </SidebarSection>

      </div>

      {/* Footer / Logout */}
      <div className="p-4 border-t border-gray-200">
         <button 
           className={`
             flex items-center gap-3 w-full px-3 py-2 rounded-lg 
             text-gray-600 hover:bg-red-50 hover:text-red-600 transition-colors
             ${isCollapsed ? 'justify-center' : ''}
           `}
           title="Logout"
           onClick={handleLogout} 
         >
           <LogOut size={20} />
           {!isCollapsed && <span className="font-medium">Logout</span>}
         </button>
      </div>

    </aside>
  );
};
