import { useEffect, useState } from 'react'
import { MiningView } from './components/MiningView'
import { useWebSocket } from './hooks/useWebSocket'
import { useTelegram } from './hooks/useTelegram'

// API URL - change this to your Railway backend URL
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'
const WS_URL = import.meta.env.VITE_WS_URL || 'ws://localhost:8000'

export interface GameState {
  skill_type: string
  level: number
  xp: number
  xp_in_level: number
  xp_needed: number
  current_action: string | null
  action_started: string | null
  available_ores: OreData[]
  inventory: Record<string, number>
}

export interface OreData {
  id: string
  name: string
  level_required: number
  xp: number
  mining_time: number
  ascii: string
  color: string
  description: string
  quantity: number
  unlocked: boolean
}

function App() {
  const { user, webApp } = useTelegram()
  const [gameState, setGameState] = useState<GameState | null>(null)
  const [miningProgress, setMiningProgress] = useState(0)
  const [notification, setNotification] = useState<string | null>(null)
  const [levelUpAnimation, setLevelUpAnimation] = useState(false)

  // Get user ID (use Telegram ID or fallback for testing)
  const userId = user?.id || 12345

  const { sendMessage, isConnected } = useWebSocket({
    url: `${WS_URL}/ws/${userId}`,
    onMessage: (data) => {
      switch (data.type) {
        case 'status':
          setGameState(data.data)
          break
        case 'mining_tick':
          setMiningProgress(data.progress)
          break
        case 'ore_mined':
          setMiningProgress(0)
          setNotification(`+1 ${data.ore_name}! +${data.xp_gained} XP`)
          // Update game state
          setGameState(prev => prev ? {
            ...prev,
            xp: data.total_xp,
            level: data.level,
            xp_in_level: data.xp_in_level,
            xp_needed: data.xp_needed,
            inventory: {
              ...prev.inventory,
              [data.ore_id]: data.ore_quantity
            }
          } : null)
          setTimeout(() => setNotification(null), 2000)
          break
        case 'level_up':
          setLevelUpAnimation(true)
          setNotification(`LEVEL UP! Mining Level ${data.new_level}!`)
          setTimeout(() => {
            setLevelUpAnimation(false)
            setNotification(null)
          }, 3000)
          break
        case 'mining_started':
          setGameState(prev => prev ? {
            ...prev,
            current_action: data.ore_id
          } : null)
          break
        case 'mining_stopped':
          setMiningProgress(0)
          setGameState(prev => prev ? {
            ...prev,
            current_action: null
          } : null)
          break
        case 'error':
          setNotification(data.message)
          setTimeout(() => setNotification(null), 3000)
          break
      }
    }
  })

  // Expand Telegram Mini App
  useEffect(() => {
    if (webApp) {
      webApp.expand()
      webApp.ready()
    }
  }, [webApp])

  const handleStartMining = (oreId: string) => {
    sendMessage({ action: 'start_mining', ore: oreId })
  }

  const handleStopMining = () => {
    sendMessage({ action: 'stop_mining' })
  }

  if (!isConnected) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="ascii-art text-2xl mb-4">
{`
  ⛏️
 /|\\
 / \\
`}
          </div>
          <p className="font-pixel text-sm">Connecting...</p>
        </div>
      </div>
    )
  }

  if (!gameState) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin text-4xl mb-4">⛏️</div>
          <p className="font-pixel text-sm">Loading game...</p>
        </div>
      </div>
    )
  }

  return (
    <div className={`min-h-screen pb-20 ${levelUpAnimation ? 'level-up-flash' : ''}`}>
      {/* Header */}
      <header className="sticky top-0 z-50 bg-[#16213e] border-b border-gray-700 px-4 py-3">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <span className="text-2xl">⛏️</span>
            <div>
              <h1 className="font-pixel text-xs text-yellow-400">MINING</h1>
              <p className="text-xs text-gray-400">Idle Game</p>
            </div>
          </div>
          <div className="text-right">
            <p className="font-pixel text-sm text-yellow-400">Lv.{gameState.level}</p>
            <p className="text-xs text-gray-400">
              {gameState.xp.toLocaleString()} XP
            </p>
          </div>
        </div>
      </header>

      {/* Notification */}
      {notification && (
        <div className="fixed top-16 left-1/2 -translate-x-1/2 z-50 pop-in">
          <div className="bg-yellow-500 text-black px-4 py-2 rounded-lg font-pixel text-xs shadow-lg">
            {notification}
          </div>
        </div>
      )}

      {/* Main Content */}
      <main className="p-4">
        <MiningView
          gameState={gameState}
          miningProgress={miningProgress}
          onStartMining={handleStartMining}
          onStopMining={handleStopMining}
        />
      </main>

      {/* Connection Status */}
      <div className="fixed bottom-0 left-0 right-0 bg-[#16213e] border-t border-gray-700 px-4 py-2">
        <div className="flex items-center justify-between text-xs">
          <span className="text-gray-400">
            {user?.first_name || 'Player'}
          </span>
          <span className={`flex items-center gap-1 ${isConnected ? 'text-green-400' : 'text-red-400'}`}>
            <span className={`w-2 h-2 rounded-full ${isConnected ? 'bg-green-400' : 'bg-red-400'}`}></span>
            {isConnected ? 'Connected' : 'Disconnected'}
          </span>
        </div>
      </div>
    </div>
  )
}

export default App
