"use client";

import { ChatWindow } from '@/components/user_dashboard/conversations/ChatWindow';
import { ConversationList } from '@/components/user_dashboard/conversations/ConversationList';
import { useEffect, useState } from 'react';

export default function ConversationsPage() {
  const [conversations, setConversations] = useState<any[]>([]);
  const [loadingList, setLoadingList] = useState(true);
  
  const [selectedId, setSelectedId] = useState<string | null>(null);
  const [messages, setMessages] = useState<any[]>([]);
  const [fallbackData, setFallbackData] = useState<any>(null);
  const [loadingChat, setLoadingChat] = useState(false);
  
  const [filter, setFilter] = useState('all');
  const [searchQuery, setSearchQuery] = useState('');
  
  // Chat state
  const [isAgentEnabled, setIsAgentEnabled] = useState(true);

  // Initial Fetch conversations
  const fetchConversations = async (page = 1, limit = 50) => {
     setLoadingList(true);
     try {
         const res = await fetch(`/api/conversation?page=${page}&limit=${limit}`);
         if (!res.ok) throw new Error('Failed to fetch conversations');
         const result = await res.json();
         if (result.status === 'success') {
             setConversations(result.data.conversations || []);
         }
     } catch (err) {
         console.error('Error fetching conversations:', err);
         alert("Failed to load conversation list.");
     } finally {
         setLoadingList(false);
     }
  };

  useEffect(() => {
    fetchConversations();
  }, []);

  // Filter Logic
  const filteredConversations = conversations.filter(conv => {
    const matchesFilter = 
      filter === 'all' ? true :
      filter === 'human_needed' ? conv.need_human === true :
      filter === 'ai_handled' ? conv.need_human === false : true;
    
    const matchesSearch = 
      conv.username?.toLowerCase().includes(searchQuery.toLowerCase()) ||
      conv.phone_number?.includes(searchQuery);

    return matchesFilter && matchesSearch;
  });

  // Select Conversation Logic
  const handleSelectConversation = async (id: string) => {
    setSelectedId(id);
    setLoadingChat(true);
    setMessages([]);
    setFallbackData(null);
    setIsAgentEnabled(true); // default true before fetching status
    
    const conversation = conversations.find(c => c.id === id);
    if (!conversation) return;

    try {
        let endpoint = `/api/conversation/message?id=${id}`;
        // if needs human, fetch fallback endpoint to get confidence info
        if (conversation.need_human) {
            endpoint = `/api/conversation/fallback?id=${id}`;
        }
        
        const res = await fetch(endpoint);
        if (!res.ok) throw new Error('Failed to load chat details');
        const result = await res.json();
        
        if (result.status === 'success') {
            setMessages(result.data.messages || []);
            setIsAgentEnabled(result.data.convStatusAgent ?? true); // Sync agent status switch
            setFallbackData(result.data.fallback || null);
        }
    } catch (err) {
        console.error('Error fetching chat details:', err);
        alert('Failed to load the conversation messages.');
    } finally {
        setLoadingChat(false);
    }
  };

  const handleSendMessage = async (text: string) => {
    if (!selectedId) return;
    
    // Add optimistic message to UI temporarily
    const optimisticMessage = {
        id: 'temp-' + Date.now(),
        content: text,
        sender_type: 'human_admin',
        created_at: new Date().toISOString()
    };
    setMessages(prev => [...prev, optimisticMessage]);

    try {
        const res = await fetch(`/api/conversation/message?id=${selectedId}`, {
            method: 'POST',
            body: JSON.stringify({text_message: text}),
            headers: { 'Content-Type': 'application/json' }
        });
        
        if (!res.ok) throw new Error("Failed to send message");
        // We could refetch or just rely on the fallback structure if the API returns the saved message 
        // For now, if no error is thrown, the optimistic message stays valid (we can re-fetch just in case)
        
        // Re-fetch chat data to get correct ID mapping
        const refetchRes = await fetch(`/api/conversation/message?id=${selectedId}`);
        const result = await refetchRes.json();
        if (result.status === 'success') setMessages(result.data.messages || []);
        
    } catch (err) {
        console.error('Error sending message:', err);
        alert('Failed to send the message. Please try again.');
        // Filter out optimistic message if failed
        setMessages(prev => prev.filter(m => m.id !== optimisticMessage.id));
    }
  };

  const handleToggleAgent = async (enabled: boolean) => {
      if (!selectedId) return;
      const originalState = isAgentEnabled;
      setIsAgentEnabled(enabled); // Optimistically swap UI
      
      try {
          const res = await fetch(`/api/conversation?id=${selectedId}`, {
              method: 'PUT',
              body: JSON.stringify({ agentStatus: enabled }),
              headers: { 'Content-Type': 'application/json' }
          });
          if (!res.ok) throw new Error("Failed to toggle agent status.");
      } catch (err) {
          console.error('Error toggling agent:', err);
          alert('Failed to update agent status.');
          setIsAgentEnabled(originalState); // Revert UI
      }
  };

  const selectedConversation = conversations.find(c => c.id === selectedId);

  return (
    <>
      <div className="h-[calc(100vh-100px)] bg-white rounded-2xl shadow-sm border border-gray-200 overflow-hidden flex">
        
        {/* Left Panel: List */}
        <div className="w-1/3 min-w-[320px] max-w-[400px] h-full flex flex-col">
           <ConversationList
             conversations={filteredConversations}
             selectedId={selectedId}
             onSelect={handleSelectConversation}
             isLoading={loadingList}
             filter={filter}
             onFilterChange={setFilter}
             searchQuery={searchQuery}
             onSearchChange={setSearchQuery}
           />
        </div>

        {/* Right Panel: Chat */}
        <div className="flex-1 h-full min-w-0">
           <ChatWindow
             conversationId={selectedId}
             username={selectedConversation?.username || ''}
             phoneNumber={selectedConversation?.phone_number || ''}
             status={selectedConversation?.need_human ? 'pending' : 'active'}
             fallback={fallbackData}
             messages={messages}
             isAgentEnabled={isAgentEnabled}
             onToggleAgent={handleToggleAgent}
             onSendMessage={handleSendMessage}
             isLoading={loadingChat}
           />
        </div>

      </div>
    </>
  );
}
