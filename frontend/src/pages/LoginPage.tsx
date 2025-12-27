import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Bot, KeyRound, User } from 'lucide-react';

export function LoginPage() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleLogin = (e: React.FormEvent) => {
    e.preventDefault();
    if (username === 'user' && password === 'user') {
      localStorage.setItem('isAuthenticated', 'true');
      navigate('/');
    } else {
      setError('Invalid credentials');
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-background px-4">
      <div className="w-full max-w-md bg-card border border-border rounded-xl shadow-xl overflow-hidden p-8 animate-in zoom-in-95 duration-500">
        <div className="flex flex-col items-center mb-8">
          <div className="h-12 w-12 bg-primary rounded-full flex items-center justify-center mb-4 text-primary-foreground shadow-lg">
            <Bot className="w-7 h-7" />
          </div>
          <h1 className="text-3xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-primary to-primary/60">
            CogniFlow
          </h1>
          <p className="text-muted-foreground mt-2">Sign in to your dashboard</p>
        </div>

        <form onSubmit={handleLogin} className="space-y-6">
          <div>
            <label className="block text-sm font-medium text-foreground mb-1.5 ml-1">
              Username
            </label>
            <div className="relative">
              <User className="absolute left-3 top-2.5 h-5 w-5 text-muted-foreground" />
              <input
                type="text"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                className="w-full pl-10 pr-4 py-2 bg-input border border-input rounded-lg focus:ring-2 focus:ring-ring focus:border-input transition-all"
                placeholder="Enter username"
              />
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-foreground mb-1.5 ml-1">
              Password
            </label>
            <div className="relative">
              <KeyRound className="absolute left-3 top-2.5 h-5 w-5 text-muted-foreground" />
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="w-full pl-10 pr-4 py-2 bg-input border border-input rounded-lg focus:ring-2 focus:ring-ring focus:border-input transition-all"
                placeholder="Enter password"
              />
            </div>
          </div>

          {error && (
            <div className="p-3 rounded-lg bg-destructive/10 text-destructive text-sm text-center font-medium animate-pulse">
              {error}
            </div>
          )}

          <button
            type="submit"
            className="w-full bg-primary text-primary-foreground py-2.5 rounded-lg font-semibold shadow-lg hover:shadow-primary/20 hover:bg-primary/90 transition-all active:scale-95"
          >
            Sign In
          </button>
        </form>

        <div className="mt-6 text-center text-xs text-muted-foreground">
          <p>Demo Credentials: user / user</p>
        </div>
      </div>
    </div>
  );
}
