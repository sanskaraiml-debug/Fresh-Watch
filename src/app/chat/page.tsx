"use client";

import React, { useState, useEffect, useRef } from "react";
import {
  Bot,
  Send,
  Phone,
  PhoneOff,
  Mic,
  MicOff,
  Volume2,
  VolumeX,
  Sparkles,
  RotateCcw,
  CheckCircle2,
  Leaf,
  Globe,
  Radio,
} from "lucide-react";

interface Message {
  id: string;
  role: "user" | "assistant";
  content: string;
  timestamp: string;
}

export default function ChatAssistantPage() {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: "m0",
      role: "assistant",
      content:
        "Hello! I am your Inventory Analysis AI Calling Assistant. I have live access to your supermarket's real-time inventory, stock counts, shelf-life dates, and Random Forest expiry predictions. You can speak to me or type your questions in English, Hindi, Spanish, or any language you prefer.",
      timestamp: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
    },
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  // Calling Simulation Mode
  const [isCallActive, setIsCallActive] = useState(false);
  const [isSpeaking, setIsSpeaking] = useState(false);
  const [isListening, setIsListening] = useState(false);
  const [callDuration, setCallDuration] = useState(0);
  const [speechEnabled, setSpeechEnabled] = useState(true);

  const messagesEndRef = useRef<HTMLDivElement>(null);
  const recognitionRef = useRef<any>(null);

  // Auto scroll
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  // Call timer
  useEffect(() => {
    let timer: any;
    if (isCallActive) {
      timer = setInterval(() => {
        setCallDuration((prev) => prev + 1);
      }, 1000);
    } else {
      setCallDuration(0);
    }
    return () => clearInterval(timer);
  }, [isCallActive]);

  // Speech Recognition Setup
  useEffect(() => {
    if (typeof window !== "undefined") {
      const SpeechRecognition =
        (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;
      if (SpeechRecognition) {
        const recognition = new SpeechRecognition();
        recognition.continuous = false;
        recognition.interimResults = false;
        recognition.lang = "en-US";

        recognition.onresult = (event: any) => {
          const transcript = event.results[0][0].transcript;
          if (transcript) {
            handleSendMessage(transcript);
          }
          setIsListening(false);
        };

        recognition.onerror = () => {
          setIsListening(false);
        };

        recognition.onend = () => {
          setIsListening(false);
        };

        recognitionRef.current = recognition;
      }
    }
  }, []);

  // Text to Speech
  const speakText = (text: string) => {
    if (!speechEnabled || typeof window === "undefined" || !("speechSynthesis" in window)) {
      return;
    }
    window.speechSynthesis.cancel();

    // Clean markdown symbols for cleaner vocalization
    const plainText = text
      .replace(/[*#_`~>]/g, "")
      .replace(/•/g, "")
      .replace(/₹/g, "rupees ");

    const utterance = new SpeechSynthesisUtterance(plainText);
    utterance.rate = 1.0;
    utterance.pitch = 1.0;

    // Detect Hindi
    if (/[\u0900-\u097F]/.test(plainText)) {
      utterance.lang = "hi-IN";
    } else if (/[áéíóúñ¿¡]/i.test(plainText)) {
      utterance.lang = "es-ES";
    } else {
      utterance.lang = "en-US";
    }

    utterance.onstart = () => setIsSpeaking(true);
    utterance.onend = () => setIsSpeaking(false);
    utterance.onerror = () => setIsSpeaking(false);

    window.speechSynthesis.speak(utterance);
  };

  const handleSendMessage = async (userText: string) => {
    const text = userText.trim();
    if (!text || loading) return;

    const userMsg: Message = {
      id: `u-${Date.now()}`,
      role: "user",
      content: text,
      timestamp: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
    };

    setMessages((prev) => [...prev, userMsg]);
    setInput("");
    setLoading(true);

    try {
      const historyPayload = messages.slice(-6).map((m) => ({
        role: m.role,
        content: m.content,
      }));

      const res = await fetch("/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          prompt: text,
          history: historyPayload,
        }),
      });

      const data = await res.json();
      if (res.ok && data.success) {
        const assistantMsg: Message = {
          id: `a-${Date.now()}`,
          role: "assistant",
          content: data.response,
          timestamp: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
        };
        setMessages((prev) => [...prev, assistantMsg]);
        speakText(data.response);
      } else {
        throw new Error(data.error || "Failed to get response");
      }
    } catch (err: any) {
      const errorMsg: Message = {
        id: `e-${Date.now()}`,
        role: "assistant",
        content:
          "I encountered an issue retrieving the live inventory. Please check that the server is online.",
        timestamp: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
      };
      setMessages((prev) => [...prev, errorMsg]);
    } finally {
      setLoading(false);
    }
  };

  const toggleVoiceInput = () => {
    if (!recognitionRef.current) {
      alert("Speech recognition is not supported in this browser. You can type your query.");
      return;
    }
    if (isListening) {
      recognitionRef.current.stop();
      setIsListening(false);
    } else {
      setIsListening(true);
      recognitionRef.current.start();
    }
  };

  const toggleCallMode = () => {
    if (isCallActive) {
      setIsCallActive(false);
      window.speechSynthesis?.cancel();
      setIsSpeaking(false);
      if (isListening && recognitionRef.current) {
        recognitionRef.current.stop();
        setIsListening(false);
      }
    } else {
      setIsCallActive(true);
      speakText("Inventory Analysis AI calling assistant connected. How can I help with your supermarket inventory?");
    }
  };

  const formatCallTime = (secs: number) => {
    const mins = Math.floor(secs / 60);
    const remainingSecs = secs % 60;
    return `${mins.toString().padStart(2, "0")}:${remainingSecs.toString().padStart(2, "0")}`;
  };

  const quickPrompts = [
    "How many stocks of pulses left in my supermarket?",
    "When is my Basmati rice going to expire?",
    "Which products are expiring in the next 3 days?",
    "दुकान में दालों का कितना स्टॉक बचा है?",
    "Recommend discounts for high-risk dairy items",
    "¿Cuáles son los productos con mayor riesgo de caducidad?",
  ];

  return (
    <div className="max-w-5xl mx-auto px-4 sm:px-6 py-6 space-y-4">
      {/* Top Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3 pb-3 border-b border-slate-200">
        <div>
          <h1 className="text-2xl font-bold tracking-tight text-slate-900 flex items-center gap-2">
            <Bot className="h-6 w-6 text-emerald-800" />
            AI Calling Assistant
          </h1>
          <p className="text-xs text-slate-500 mt-0.5">
            Real-time grounded conversational voice & chat inventory intelligence across Hindi, English, Spanish, and more.
          </p>
        </div>

        {/* Call Toggle Button */}
        <div className="flex items-center gap-2">
          <button
            onClick={() => setSpeechEnabled(!speechEnabled)}
            className={`p-2 rounded-xl border transition-colors ${
              speechEnabled
                ? "bg-emerald-50 text-emerald-800 border-emerald-200"
                : "bg-slate-100 text-slate-400 border-slate-200"
            }`}
            title={speechEnabled ? "Voice audio enabled" : "Voice audio muted"}
          >
            {speechEnabled ? <Volume2 className="h-4 w-4" /> : <VolumeX className="h-4 w-4" />}
          </button>

          <button
            onClick={toggleCallMode}
            className={`flex items-center gap-2 px-4 py-2 rounded-xl text-xs font-bold transition-all shadow-md ${
              isCallActive
                ? "bg-red-600 hover:bg-red-700 text-white animate-pulse"
                : "bg-emerald-800 hover:bg-emerald-700 text-white"
            }`}
          >
            {isCallActive ? (
              <>
                <PhoneOff className="h-4 w-4" />
                <span>End Call ({formatCallTime(callDuration)})</span>
              </>
            ) : (
              <>
                <Phone className="h-4 w-4" />
                <span>Start AI Voice Call</span>
              </>
            )}
          </button>
        </div>
      </div>

      {/* Voice Call Active Banner (Gemini-style visual pulse) */}
      {isCallActive && (
        <div className="rounded-2xl bg-gradient-to-r from-emerald-900 to-emerald-800 text-white p-5 shadow-lg flex flex-col sm:flex-row items-center justify-between gap-4 border border-emerald-700">
          <div className="flex items-center gap-4">
            <div className="relative flex h-14 w-14 items-center justify-center rounded-2xl bg-emerald-700/80 border border-emerald-500/50 shadow-inner">
              <Bot className="h-7 w-7 text-emerald-200" />
              {isSpeaking && (
                <span className="absolute -top-1 -right-1 flex h-4 w-4">
                  <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75" />
                  <span className="relative inline-flex rounded-full h-4 w-4 bg-emerald-500" />
                </span>
              )}
            </div>

            <div>
              <div className="flex items-center gap-2">
                <span className="font-bold text-base">Voice Call Live</span>
                <span className="text-xs px-2 py-0.5 rounded-full bg-emerald-700 font-mono text-emerald-200">
                  {formatCallTime(callDuration)}
                </span>
              </div>
              <p className="text-xs text-emerald-200 mt-0.5">
                {isSpeaking
                  ? "AI Assistant is speaking..."
                  : isListening
                  ? "Listening to your voice..."
                  : "Tap the microphone to speak, or ask any stock question."}
              </p>
            </div>
          </div>

          <div className="flex items-center gap-3">
            <button
              onClick={toggleVoiceInput}
              className={`flex items-center gap-1.5 px-4 py-2 rounded-xl text-xs font-bold transition-all shadow-sm ${
                isListening
                  ? "bg-amber-500 text-slate-900 animate-bounce"
                  : "bg-white text-emerald-950 hover:bg-emerald-50"
              }`}
            >
              {isListening ? <MicOff className="h-4 w-4" /> : <Mic className="h-4 w-4 text-emerald-700" />}
              <span>{isListening ? "Listening..." : "Speak Query"}</span>
            </button>

            <button
              onClick={toggleCallMode}
              className="p-2.5 rounded-xl bg-red-600 hover:bg-red-700 text-white transition-colors"
              title="Hang up call"
            >
              <PhoneOff className="h-4 w-4" />
            </button>
          </div>
        </div>
      )}

      {/* Suggested Quick Prompt Chips */}
      <div className="flex items-center gap-2 overflow-x-auto pb-1 scrollbar-none">
        <span className="text-[11px] font-semibold text-slate-500 shrink-0 uppercase tracking-wider">
          Suggested Queries:
        </span>
        {quickPrompts.map((chip, idx) => (
          <button
            key={idx}
            onClick={() => handleSendMessage(chip)}
            className="shrink-0 px-3 py-1 rounded-full border border-slate-200 bg-white hover:bg-emerald-50 hover:border-emerald-300 text-xs text-slate-700 hover:text-emerald-900 transition-colors shadow-2xs"
          >
            {chip}
          </button>
        ))}
      </div>

      {/* Chat Messages Box */}
      <div className="rounded-2xl border border-slate-200 bg-white shadow-xs flex flex-col h-[520px] overflow-hidden">
        {/* Messages List */}
        <div className="flex-1 overflow-y-auto p-4 sm:p-6 space-y-4">
          {messages.map((m) => {
            const isUser = m.role === "user";
            return (
              <div
                key={m.id}
                className={`flex gap-3 ${isUser ? "justify-end" : "justify-start"}`}
              >
                {!isUser && (
                  <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-xl bg-emerald-800 text-emerald-200 text-xs shadow-xs">
                    <Leaf className="h-4 w-4 text-emerald-300" />
                  </div>
                )}

                <div
                  className={`max-w-[82%] sm:max-w-[75%] rounded-2xl p-4 text-xs sm:text-sm leading-relaxed shadow-2xs ${
                    isUser
                      ? "bg-emerald-800 text-white rounded-br-none"
                      : "bg-slate-50 border border-slate-200/80 text-slate-800 rounded-bl-none"
                  }`}
                >
                  <div className="whitespace-pre-line">{m.content}</div>
                  <div
                    className={`mt-2 text-[10px] text-right ${
                      isUser ? "text-emerald-200/70" : "text-slate-400"
                    }`}
                  >
                    {m.timestamp}
                  </div>
                </div>
              </div>
            );
          })}

          {loading && (
            <div className="flex gap-3 justify-start">
              <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-xl bg-emerald-800 text-emerald-200 text-xs shadow-xs">
                <Leaf className="h-4 w-4 text-emerald-300" />
              </div>
              <div className="rounded-2xl p-4 bg-slate-50 border border-slate-200/80 text-slate-500 rounded-bl-none flex items-center gap-2 text-xs">
                <div className="flex space-x-1">
                  <div className="h-2 w-2 rounded-full bg-emerald-600 animate-bounce [animation-delay:-0.3s]" />
                  <div className="h-2 w-2 rounded-full bg-emerald-600 animate-bounce [animation-delay:-0.15s]" />
                  <div className="h-2 w-2 rounded-full bg-emerald-600 animate-bounce" />
                </div>
                <span>Checking supermarket inventory database...</span>
              </div>
            </div>
          )}

          <div ref={messagesEndRef} />
        </div>

        {/* Chat Input Bar */}
        <div className="p-3 border-t border-slate-200 bg-slate-50/70">
          <form
            onSubmit={(e) => {
              e.preventDefault();
              handleSendMessage(input);
            }}
            className="flex items-center gap-2"
          >
            <button
              type="button"
              onClick={toggleVoiceInput}
              className={`p-2.5 rounded-xl border transition-colors ${
                isListening
                  ? "bg-amber-500 text-slate-900 border-amber-600 animate-pulse"
                  : "bg-white text-slate-600 hover:text-emerald-800 hover:border-emerald-300 border-slate-200"
              }`}
              title="Speak voice query"
            >
              {isListening ? <MicOff className="h-4 w-4" /> : <Mic className="h-4 w-4" />}
            </button>

            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Ask anything (e.g. 'How much Toor Dal stock is left?', 'Any items expiring this week?')..."
              className="flex-1 rounded-xl border border-slate-200 bg-white py-2.5 px-4 text-xs sm:text-sm text-slate-800 placeholder-slate-400 focus:border-emerald-500 focus:outline-none focus:ring-1 focus:ring-emerald-500"
            />

            <button
              type="submit"
              disabled={!input.trim() || loading}
              className="flex items-center justify-center h-10 w-10 rounded-xl bg-emerald-800 text-white hover:bg-emerald-700 transition-colors disabled:opacity-50 shadow-sm shrink-0"
              title="Send query"
            >
              <Send className="h-4 w-4" />
            </button>
          </form>
        </div>
      </div>
    </div>
  );
}
