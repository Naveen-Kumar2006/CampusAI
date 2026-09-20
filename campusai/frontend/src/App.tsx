import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import { MessageCircle, X, Send, Menu, ChevronRight, MapPin, Phone, Mail, BookOpen, Users, Calendar, Award, Building2 } from 'lucide-react';

// --- Chatbot Component ---
function Chatbot() {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState<{role: 'user'|'ai', text: string}[]>([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const sendMessage = async () => {
    if (!input.trim()) return;
    setMessages(prev => [...prev, { role: 'user', text: input }]);
    const currentInput = input;
    setInput('');
    setIsLoading(true);

    try {
      const response = await fetch('http://localhost:8000/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: currentInput })
      });
      const data = await response.json();
      setMessages(prev => [...prev, { role: 'ai', text: data.answer }]);
    } catch (error) {
      setMessages(prev => [...prev, { role: 'ai', text: "Error connecting to server." }]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="fixed bottom-6 right-6 z-50">
      {isOpen ? (
        <div className="w-80 sm:w-96 h-[30rem] bg-white rounded-xl shadow-2xl flex flex-col border border-gray-200 overflow-hidden transform transition-all duration-300 ease-in-out">
          <div className="bg-blue-900 text-white p-4 flex justify-between items-center shadow-md">
            <div className="flex items-center gap-2">
              <MessageCircle size={20} className="text-cyan-400" />
              <h3 className="font-bold tracking-wide">CampusAI Assistant</h3>
            </div>
            <button onClick={() => setIsOpen(false)} className="hover:bg-blue-800 p-1 rounded transition-colors"><X size={20} /></button>
          </div>
          <div className="flex-1 p-4 overflow-y-auto bg-slate-50 flex flex-col gap-3">
            <div className="bg-white border border-gray-200 shadow-sm p-3 rounded-2xl rounded-tl-sm max-w-[85%] self-start text-sm text-slate-700">
              👋 Hello! I'm CampusAI. How can I help you today?
            </div>
            {messages.map((msg, idx) => (
              <div key={idx} className={`p-3 rounded-2xl max-w-[85%] text-sm shadow-sm ${msg.role === 'user' ? 'bg-blue-600 text-white self-end rounded-tr-sm' : 'bg-white border border-gray-200 text-slate-700 self-start rounded-tl-sm'}`}>
                {msg.text}
              </div>
            ))}
            {isLoading && <div className="text-sm text-slate-500 italic flex items-center gap-2 ml-2">
              <div className="w-2 h-2 bg-blue-400 rounded-full animate-bounce"></div>
              <div className="w-2 h-2 bg-blue-400 rounded-full animate-bounce delay-75"></div>
              <div className="w-2 h-2 bg-blue-400 rounded-full animate-bounce delay-150"></div>
            </div>}
          </div>
          <div className="p-3 border-t border-gray-200 bg-white flex gap-2">
            <input 
              type="text" 
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && sendMessage()}
              placeholder="Ask me anything..."
              className="flex-1 border border-gray-300 bg-slate-50 p-3 rounded-full text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 transition-shadow"
            />
            <button onClick={sendMessage} className="bg-blue-600 text-white p-3 rounded-full hover:bg-blue-700 transition-colors shadow-md flex items-center justify-center">
              <Send size={18} />
            </button>
          </div>
        </div>
      ) : (
        <button 
          onClick={() => setIsOpen(true)}
          className="bg-blue-900 text-white px-6 py-4 rounded-full shadow-[0_8px_30px_rgb(0,0,0,0.12)] hover:shadow-[0_8px_30px_rgb(30,58,138,0.4)] hover:bg-blue-800 hover:-translate-y-1 transform transition-all duration-300 flex items-center gap-3 font-bold text-lg group"
        >
          <MessageCircle size={28} className="text-cyan-400 group-hover:scale-110 transition-transform" />
          <span className="hidden sm:inline">Ask CampusAI</span>
        </button>
      )}
    </div>
  );
}

// --- Layouts & Pages ---
function Navbar() {
  const [isScrolled, setIsScrolled] = useState(false);
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  useEffect(() => {
    const handleScroll = () => {
      setIsScrolled(window.scrollY > 10);
    };
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  return (
    <nav className={`fixed w-full top-0 z-40 transition-all duration-300 ${isScrolled ? 'bg-white text-slate-800 shadow-md py-3' : 'bg-blue-900 text-white py-4 shadow-lg'}`}>
      <div className="max-w-7xl mx-auto px-4 md:px-8">
        <div className="flex justify-between items-center">
          <Link to="/" className="flex items-center gap-2 group">
            <div className={`w-10 h-10 rounded-lg flex items-center justify-center font-bold text-xl transition-colors ${isScrolled ? 'bg-blue-900 text-white' : 'bg-white text-blue-900'}`}>
              CAI
            </div>
            <span className="text-2xl font-bold tracking-tight">Campus<span className={isScrolled ? 'text-blue-600' : 'text-cyan-400'}>AI</span></span>
          </Link>
          
          {/* Desktop Menu */}
          <div className="hidden md:flex gap-8 items-center font-medium">
            <Link to="/" className={`transition-colors hover:text-blue-500 ${isScrolled ? 'text-slate-600' : 'text-gray-100'}`}>Home</Link>
            <Link to="/about" className={`transition-colors hover:text-blue-500 ${isScrolled ? 'text-slate-600' : 'text-gray-100'}`}>About</Link>
            <Link to="/departments" className={`transition-colors hover:text-blue-500 ${isScrolled ? 'text-slate-600' : 'text-gray-100'}`}>Departments</Link>
            <Link to="/academics" className={`transition-colors hover:text-blue-500 ${isScrolled ? 'text-slate-600' : 'text-gray-100'}`}>Academics</Link>
            <Link to="/placements" className={`transition-colors hover:text-blue-500 ${isScrolled ? 'text-slate-600' : 'text-gray-100'}`}>Placements</Link>
            <Link to="/student" className={`px-5 py-2.5 rounded-lg font-semibold transition-all transform hover:-translate-y-0.5 shadow-sm ${isScrolled ? 'bg-blue-600 text-white hover:bg-blue-700 hover:shadow-md' : 'bg-cyan-500 text-blue-900 hover:bg-cyan-400'}`}>Login</Link>
          </div>
          
          {/* Mobile Toggle */}
          <button className="md:hidden" onClick={() => setMobileMenuOpen(!mobileMenuOpen)}>
            <Menu size={28} />
          </button>
        </div>
      </div>
      
      {/* Mobile Menu */}
      {mobileMenuOpen && (
        <div className={`md:hidden absolute top-full left-0 w-full shadow-xl border-t flex flex-col ${isScrolled ? 'bg-white text-slate-800 border-gray-200' : 'bg-blue-800 text-white border-blue-700'}`}>
          <Link to="/" className="p-4 border-b border-opacity-10" onClick={() => setMobileMenuOpen(false)}>Home</Link>
          <Link to="/about" className="p-4 border-b border-opacity-10" onClick={() => setMobileMenuOpen(false)}>About</Link>
          <Link to="/departments" className="p-4 border-b border-opacity-10" onClick={() => setMobileMenuOpen(false)}>Departments</Link>
          <Link to="/academics" className="p-4 border-b border-opacity-10" onClick={() => setMobileMenuOpen(false)}>Academics</Link>
          <Link to="/placements" className="p-4 border-b border-opacity-10" onClick={() => setMobileMenuOpen(false)}>Placements</Link>
          <Link to="/student" className="p-4 bg-blue-600 text-white font-bold text-center" onClick={() => setMobileMenuOpen(false)}>Login</Link>
        </div>
      )}
    </nav>
  );
}

function Home() {
  const [announcements, setAnnouncements] = useState<any[]>([]);
  const [events, setEvents] = useState<any[]>([]);
  const [departments, setDepartments] = useState<any[]>([]);

  useEffect(() => {
    fetch('http://localhost:8000/api/announcements').then(r => r.json()).then(data => setAnnouncements(data.slice(0, 3))).catch(e => console.error(e));
    fetch('http://localhost:8000/api/events').then(r => r.json()).then(data => setEvents(data.slice(0, 3))).catch(e => console.error(e));
    fetch('http://localhost:8000/api/departments').then(r => r.json()).then(data => setDepartments(data.slice(0, 4))).catch(e => console.error(e));
  }, []);

  return (
    <div className="pt-16">
      {/* Hero */}
      <div className="relative bg-blue-900 text-white min-h-[85vh] flex items-center justify-center text-center bg-cover bg-center overflow-hidden" 
           style={{backgroundImage: "linear-gradient(to bottom, rgba(15, 23, 42, 0.7), rgba(15, 23, 42, 0.9)), url('https://images.unsplash.com/photo-1541339907198-e08756dedf3f?ixlib=rb-4.0.3&auto=format&fit=crop&w=1920&q=80')"}}>
        <div className="relative z-10 max-w-4xl mx-auto px-4">
          <span className="inline-block py-1 px-3 rounded-full bg-blue-800/50 border border-blue-500 text-cyan-300 text-sm font-semibold mb-6 tracking-wider uppercase">Welcome to the Future</span>
          <h1 className="text-5xl md:text-7xl font-extrabold mb-6 leading-tight tracking-tight text-white drop-shadow-lg">
            Empowering the <span className="text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 to-blue-400">Engineers</span> of Tomorrow
          </h1>
          <p className="text-xl md:text-2xl text-gray-300 mb-10 font-light max-w-3xl mx-auto">
            State-of-the-art infrastructure, world-class faculty, and innovative research opportunities at CampusAI Institute of Engineering.
          </p>
          <div className="flex flex-col sm:flex-row justify-center gap-4">
            <Link to="/departments" className="bg-cyan-500 text-blue-900 px-8 py-4 rounded-lg font-bold text-lg hover:bg-cyan-400 transition-all shadow-lg hover:shadow-cyan-500/30 flex items-center justify-center gap-2">
              Explore Programs <ChevronRight size={20} />
            </Link>
            <button onClick={() => window.scrollTo({top: document.body.scrollHeight, behavior: 'smooth'})} className="bg-white/10 backdrop-blur-md border border-white/20 text-white px-8 py-4 rounded-lg font-bold text-lg hover:bg-white/20 transition-all shadow-lg flex items-center justify-center gap-2">
              Contact Us
            </button>
          </div>
        </div>
      </div>
      
      {/* Stats */}
      <div className="relative -mt-16 z-20 max-w-7xl mx-auto px-4 mb-20">
        <div className="bg-white rounded-2xl shadow-xl grid grid-cols-2 md:grid-cols-4 gap-4 p-8 border border-gray-100">
          <div className="text-center p-4 border-r border-gray-100 last:border-0 md:border-r-2 md:last:border-0">
            <div className="text-4xl md:text-5xl font-extrabold text-blue-700 mb-2">25+</div>
            <div className="text-slate-500 font-semibold text-sm uppercase tracking-wider">Years of Excellence</div>
          </div>
          <div className="text-center p-4 border-r border-gray-100 last:border-0 md:border-r-2 md:last:border-0">
            <div className="text-4xl md:text-5xl font-extrabold text-blue-700 mb-2">20+</div>
            <div className="text-slate-500 font-semibold text-sm uppercase tracking-wider">Departments</div>
          </div>
          <div className="text-center p-4 border-r border-gray-100 last:border-0 md:border-r-2 md:last:border-0">
            <div className="text-4xl md:text-5xl font-extrabold text-blue-700 mb-2">5K+</div>
            <div className="text-slate-500 font-semibold text-sm uppercase tracking-wider">Students</div>
          </div>
          <div className="text-center p-4">
            <div className="text-4xl md:text-5xl font-extrabold text-blue-700 mb-2">90%</div>
            <div className="text-slate-500 font-semibold text-sm uppercase tracking-wider">Placement Rate</div>
          </div>
        </div>
      </div>

      {/* Featured Programs */}
      <div className="py-20 bg-slate-50">
        <div className="max-w-7xl mx-auto px-4">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-slate-900 mb-4">Featured Programs</h2>
            <div className="w-24 h-1 bg-blue-600 mx-auto rounded-full mb-6"></div>
            <p className="text-lg text-slate-600 max-w-2xl mx-auto">Discover our highly sought-after engineering programs designed to meet the demands of the modern tech industry.</p>
          </div>
          
          <div className="grid md:grid-cols-3 gap-8">
            {departments.length > 0 ? departments.slice(0,3).map(dept => (
              <div key={dept.id} className="bg-white rounded-xl shadow-md border border-gray-100 overflow-hidden hover:shadow-xl transition-all group">
                <div className="h-48 bg-slate-200 overflow-hidden relative">
                  <div className="absolute inset-0 bg-blue-900/10 group-hover:bg-transparent transition-colors z-10"></div>
                  <img src={`https://images.unsplash.com/photo-1517245386807-bb43f82c33c4?auto=format&fit=crop&w=600&q=80`} alt={dept.name} className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500" />
                </div>
                <div className="p-6">
                  <h3 className="text-xl font-bold text-slate-800 mb-3">{dept.name}</h3>
                  <p className="text-slate-600 mb-4 line-clamp-3">{dept.description}</p>
                  <Link to={`/departments`} className="text-blue-600 font-semibold flex items-center gap-1 hover:text-blue-800 transition-colors">
                    Learn more <ChevronRight size={16} />
                  </Link>
                </div>
              </div>
            )) : (
              <div className="col-span-3 text-center py-10 text-slate-500">Loading programs...</div>
            )}
          </div>
          <div className="text-center mt-12">
            <Link to="/departments" className="inline-flex items-center gap-2 bg-white border-2 border-blue-600 text-blue-600 px-6 py-3 rounded-lg font-bold hover:bg-blue-50 transition-colors">
              View All Departments
            </Link>
          </div>
        </div>
      </div>

      {/* Announcements & Events Section */}
      <div className="py-20 bg-white">
        <div className="max-w-7xl mx-auto px-4 grid lg:grid-cols-2 gap-16">
          
          {/* Announcements */}
          <div>
            <div className="flex items-center justify-between mb-8">
              <h2 className="text-3xl font-bold text-slate-900 flex items-center gap-3">
                <Award className="text-blue-600" /> Latest Announcements
              </h2>
              <Link to="/announcements" className="text-blue-600 hover:underline font-medium text-sm">View All</Link>
            </div>
            <div className="flex flex-col gap-4">
              {announcements.length > 0 ? announcements.map(ann => (
                <div key={ann.id} className="bg-slate-50 border border-slate-100 p-5 rounded-xl hover:shadow-md transition-shadow flex gap-4">
                  <div className="hidden sm:flex flex-col items-center justify-center bg-white border border-slate-200 rounded-lg min-w-[70px] h-[70px] text-center">
                    <span className="text-xs text-slate-500 uppercase font-bold">{new Date(ann.date).toLocaleString('default', { month: 'short' })}</span>
                    <span className="text-2xl font-black text-blue-900 leading-none">{new Date(ann.date).getDate()}</span>
                  </div>
                  <div>
                    <div className="flex items-center gap-2 mb-1">
                      {ann.is_important && <span className="bg-red-100 text-red-700 text-xs px-2 py-0.5 rounded font-bold">URGENT</span>}
                      <span className="text-xs font-semibold text-slate-500 uppercase tracking-wider">{ann.category}</span>
                    </div>
                    <h4 className="text-lg font-bold text-slate-800 mb-2">{ann.title}</h4>
                    <p className="text-slate-600 text-sm">{ann.description}</p>
                  </div>
                </div>
              )) : <div className="text-slate-500 py-4">No announcements available.</div>}
            </div>
          </div>

          {/* Events */}
          <div>
            <div className="flex items-center justify-between mb-8">
              <h2 className="text-3xl font-bold text-slate-900 flex items-center gap-3">
                <Calendar className="text-blue-600" /> Upcoming Events
              </h2>
              <Link to="/events" className="text-blue-600 hover:underline font-medium text-sm">View All</Link>
            </div>
            <div className="flex flex-col gap-4">
              {events.length > 0 ? events.map(evt => (
                <div key={evt.id} className="bg-white border border-slate-200 p-5 rounded-xl shadow-sm hover:shadow-md transition-all flex gap-4 items-start relative overflow-hidden group">
                  <div className="absolute left-0 top-0 bottom-0 w-1 bg-cyan-500 group-hover:w-2 transition-all"></div>
                  <div className="pl-2 flex-1">
                    <h4 className="text-lg font-bold text-slate-800 mb-2">{evt.title}</h4>
                    <div className="flex flex-wrap gap-y-2 gap-x-4 text-sm text-slate-500 mb-3">
                      <span className="flex items-center gap-1"><Calendar size={14}/> {evt.date}</span>
                      <span className="flex items-center gap-1"><MapPin size={14}/> {evt.location}</span>
                    </div>
                    <p className="text-slate-600 text-sm line-clamp-2">{evt.description}</p>
                  </div>
                </div>
              )) : <div className="text-slate-500 py-4">No events scheduled.</div>}
            </div>
          </div>

        </div>
      </div>

      {/* Facilities & Placements Split */}
      <div className="py-20 bg-slate-900 text-white">
        <div className="max-w-7xl mx-auto px-4">
          <div className="grid md:grid-cols-2 gap-12 items-center">
            <div>
              <h2 className="text-3xl md:text-4xl font-bold mb-6">Exceptional Placement Record</h2>
              <p className="text-slate-400 text-lg mb-8 leading-relaxed">
                Our dedicated placement cell works tirelessly to ensure students land their dream jobs. With tie-ups with over 200+ multinational companies, CampusAI provides unparalleled career opportunities.
              </p>
              <ul className="space-y-4 mb-8">
                <li className="flex items-center gap-3"><ChevronRight className="text-cyan-400"/> Highest Package: 45 LPA</li>
                <li className="flex items-center gap-3"><ChevronRight className="text-cyan-400"/> Average Package: 12 LPA</li>
                <li className="flex items-center gap-3"><ChevronRight className="text-cyan-400"/> Top Recruiters: Google, Microsoft, Amazon</li>
              </ul>
              <Link to="/placements" className="bg-blue-600 hover:bg-blue-500 text-white px-6 py-3 rounded-lg font-bold transition-colors inline-block">
                View Placement Statistics
              </Link>
            </div>
            <div className="grid grid-cols-2 gap-4">
              <div className="space-y-4">
                <div className="bg-slate-800 p-6 rounded-xl border border-slate-700">
                  <BookOpen className="text-cyan-400 mb-4" size={32} />
                  <h4 className="font-bold text-lg mb-2">Modern Library</h4>
                  <p className="text-slate-400 text-sm">Over 100,000 resources and digital access.</p>
                </div>
                <div className="bg-slate-800 p-6 rounded-xl border border-slate-700">
                  <Building2 className="text-cyan-400 mb-4" size={32} />
                  <h4 className="font-bold text-lg mb-2">Smart Classrooms</h4>
                  <p className="text-slate-400 text-sm">Fully air-conditioned tech-enabled rooms.</p>
                </div>
              </div>
              <div className="space-y-4 mt-8">
                <div className="bg-slate-800 p-6 rounded-xl border border-slate-700">
                  <Users className="text-cyan-400 mb-4" size={32} />
                  <h4 className="font-bold text-lg mb-2">Innovation Labs</h4>
                  <p className="text-slate-400 text-sm">24/7 access to AI, IoT, and Robotics labs.</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* CTA */}
      <div className="py-24 bg-blue-600 text-center px-4">
        <h2 className="text-4xl font-bold text-white mb-6">Ready to shape your future?</h2>
        <p className="text-blue-100 text-xl max-w-2xl mx-auto mb-10">Join thousands of successful alumni who started their journey at CampusAI.</p>
        <div className="flex flex-col sm:flex-row justify-center gap-4">
          <button className="bg-white text-blue-700 px-8 py-4 rounded-lg font-bold text-lg hover:bg-gray-100 transition-colors shadow-lg">Apply Now</button>
          <button onClick={() => window.scrollTo({top: document.body.scrollHeight, behavior: 'smooth'})} className="bg-transparent border-2 border-white text-white px-8 py-4 rounded-lg font-bold text-lg hover:bg-white/10 transition-colors shadow-lg">Contact Admissions</button>
        </div>
      </div>
    </div>
  );
}

function Departments() {
  const [depts, setDepts] = React.useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  React.useEffect(() => {
    fetch('http://localhost:8000/api/departments')
      .then(r => r.json())
      .then(data => { setDepts(data); setLoading(false); })
      .catch(() => setLoading(false));
  }, []);

  return (
    <div className="pt-28 pb-20 max-w-7xl mx-auto px-4 min-h-screen">
      <div className="mb-12">
        <h1 className="text-4xl font-extrabold text-slate-900 mb-4">Academic Departments</h1>
        <p className="text-lg text-slate-600 max-w-3xl">Explore our diverse range of engineering departments, each equipped with world-class faculty and cutting-edge facilities.</p>
      </div>

      {loading ? (
        <div className="text-center py-20 text-slate-500">Loading departments...</div>
      ) : (
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
          {depts.map(d => (
            <div key={d.id} className="bg-white p-8 rounded-2xl shadow-sm border border-gray-200 hover:shadow-xl transition-all group relative overflow-hidden">
              <div className="absolute top-0 left-0 w-full h-1 bg-blue-600 group-hover:h-2 transition-all"></div>
              <h3 className="text-2xl font-bold mb-3 text-slate-800">{d.name}</h3>
              <p className="text-slate-600 mb-6 line-clamp-3">{d.description}</p>
              
              <div className="bg-slate-50 p-4 rounded-lg mb-6">
                <div className="text-sm text-slate-500 font-semibold uppercase tracking-wider mb-1">Head of Department</div>
                <div className="text-slate-800 font-medium">{d.hod}</div>
              </div>

              <div className="flex items-center justify-between text-sm text-slate-600 font-medium border-t pt-4">
                <div className="flex items-center gap-2"><Users size={16}/> {d.faculty_count} Faculty</div>
                <button className="text-blue-600 hover:text-blue-800 flex items-center gap-1 group-hover:translate-x-1 transition-transform">
                  Details <ChevronRight size={16} />
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

function PageComingSoon({ title }: { title: string }) {
  return (
    <div className="pt-32 pb-20 min-h-[70vh] flex flex-col items-center justify-center text-center px-4">
      <div className="w-20 h-20 bg-blue-100 text-blue-600 rounded-full flex items-center justify-center mb-6">
        <BookOpen size={36} />
      </div>
      <h1 className="text-4xl font-bold text-slate-900 mb-4">{title}</h1>
      <p className="text-slate-600 max-w-lg mb-8 text-lg">We are currently building this section of the CampusAI portal. Check back soon for updates.</p>
      <Link to="/" className="bg-blue-600 text-white px-6 py-3 rounded-lg font-bold hover:bg-blue-700 transition-colors">Return to Home</Link>
    </div>
  );
}

export default function App() {
  return (
    <Router>
      <div className="flex flex-col min-h-screen font-sans bg-gray-50 text-slate-800 overflow-x-hidden w-full">
        <Navbar />
        <main className="flex-1 w-full">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/departments" element={<Departments />} />
            <Route path="/about" element={<PageComingSoon title="About CampusAI" />} />
            <Route path="/academics" element={<PageComingSoon title="Academics" />} />
            <Route path="/placements" element={<PageComingSoon title="Placements" />} />
            <Route path="/announcements" element={<PageComingSoon title="Announcements" />} />
            <Route path="/events" element={<PageComingSoon title="Events" />} />
            <Route path="/student" element={<PageComingSoon title="Student Portal" />} />
            <Route path="*" element={<PageComingSoon title="Page Not Found" />} />
          </Routes>
        </main>
        
        {/* Footer */}
        <footer className="bg-slate-900 text-slate-300 pt-16 pb-8 border-t-4 border-blue-600 w-full">
          <div className="max-w-7xl mx-auto px-4 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-10 mb-12">
            <div>
              <div className="flex items-center gap-2 mb-6">
                <div className="w-8 h-8 bg-blue-600 rounded flex items-center justify-center font-bold text-white">CAI</div>
                <span className="text-2xl font-bold text-white tracking-tight">Campus<span className="text-cyan-400">AI</span></span>
              </div>
              <p className="text-slate-400 mb-6">Empowering the engineers of tomorrow through world-class education, research, and innovation.</p>
              <div className="flex gap-4">
                <a href="#" className="w-10 h-10 rounded-full bg-slate-800 flex items-center justify-center hover:bg-blue-600 transition-colors text-white"><span className="sr-only">Twitter</span>𝕏</a>
                <a href="#" className="w-10 h-10 rounded-full bg-slate-800 flex items-center justify-center hover:bg-blue-600 transition-colors text-white"><span className="sr-only">LinkedIn</span>in</a>
                <a href="#" className="w-10 h-10 rounded-full bg-slate-800 flex items-center justify-center hover:bg-blue-600 transition-colors text-white"><span className="sr-only">Instagram</span>ig</a>
              </div>
            </div>
            
            <div>
              <h4 className="text-lg font-bold text-white mb-6">Quick Links</h4>
              <ul className="space-y-3">
                <li><Link to="/about" className="hover:text-cyan-400 transition-colors">About Us</Link></li>
                <li><Link to="/academics" className="hover:text-cyan-400 transition-colors">Academics</Link></li>
                <li><Link to="/placements" className="hover:text-cyan-400 transition-colors">Placements</Link></li>
                <li><Link to="/announcements" className="hover:text-cyan-400 transition-colors">Announcements</Link></li>
                <li><Link to="/student" className="hover:text-cyan-400 transition-colors">Student Login</Link></li>
              </ul>
            </div>
            
            <div>
              <h4 className="text-lg font-bold text-white mb-6">Departments</h4>
              <ul className="space-y-3">
                <li><Link to="/departments" className="hover:text-cyan-400 transition-colors">Artificial Intelligence</Link></li>
                <li><Link to="/departments" className="hover:text-cyan-400 transition-colors">Computer Science</Link></li>
                <li><Link to="/departments" className="hover:text-cyan-400 transition-colors">Electronics & Comm.</Link></li>
                <li><Link to="/departments" className="hover:text-cyan-400 transition-colors">Mechanical Engg.</Link></li>
                <li><Link to="/departments" className="text-blue-500 hover:text-cyan-400 transition-colors font-medium">View All &rarr;</Link></li>
              </ul>
            </div>
            
            <div>
              <h4 className="text-lg font-bold text-white mb-6">Contact Us</h4>
              <ul className="space-y-4">
                <li className="flex items-start gap-3">
                  <MapPin className="text-cyan-400 mt-1 shrink-0" size={18} />
                  <span>CampusAI Institute of Engineering<br/>123 Innovation Drive<br/>Tech City, 600001</span>
                </li>
                <li className="flex items-center gap-3">
                  <Phone className="text-cyan-400 shrink-0" size={18} />
                  <span>+91 9876543210</span>
                </li>
                <li className="flex items-center gap-3">
                  <Mail className="text-cyan-400 shrink-0" size={18} />
                  <span>contact@campusai.edu.in</span>
                </li>
              </ul>
            </div>
          </div>
          
          <div className="max-w-7xl mx-auto px-4 pt-8 border-t border-slate-800 text-center text-slate-500 flex flex-col md:flex-row justify-between items-center gap-4">
            <p>© 2026 CampusAI Institute of Engineering. All rights reserved.</p>
            <div className="flex gap-6 text-sm">
              <a href="#" className="hover:text-slate-300">Privacy Policy</a>
              <a href="#" className="hover:text-slate-300">Terms of Service</a>
            </div>
          </div>
        </footer>
        <Chatbot />
      </div>
    </Router>
  );
}
