import { GameState, OreData } from '../App'
import { ProgressBar } from './ProgressBar'
import { OreCard } from './OreCard'
import { SkillPanel } from './SkillPanel'

interface MiningViewProps {
  gameState: GameState
  miningProgress: number
  onStartMining: (oreId: string) => void
  onStopMining: () => void
}

export function MiningView({ gameState, miningProgress, onStartMining, onStopMining }: MiningViewProps) {
  const currentOre = gameState.available_ores.find(o => o.id === gameState.current_action)
  const isMining = !!gameState.current_action

  return (
    <div className="space-y-4">
      {/* XP Progress */}
      <SkillPanel
        level={gameState.level}
        xp={gameState.xp}
        xpInLevel={gameState.xp_in_level}
        xpNeeded={gameState.xp_needed}
      />

      {/* Current Mining Status */}
      {isMining && currentOre && (
        <div className="bg-[#16213e] rounded-xl p-4 border border-gray-700">
          <div className="flex items-center justify-between mb-3">
            <div className="flex items-center gap-3">
              <span className="text-3xl mining-animation">⛏️</span>
              <div>
                <h3 className="font-pixel text-xs" style={{ color: currentOre.color }}>
                  {currentOre.name}
                </h3>
                <p className="text-xs text-gray-400">
                  +{currentOre.xp} XP per ore
                </p>
              </div>
            </div>
            <div className="text-right">
              <p className="font-pixel text-lg" style={{ color: currentOre.color }}>
                {gameState.inventory[currentOre.id] || 0}
              </p>
              <p className="text-xs text-gray-400">in bag</p>
            </div>
          </div>

          {/* Mining Progress Bar */}
          <ProgressBar 
            progress={miningProgress} 
            color={currentOre.color}
            showPercentage
          />

          {/* ASCII Mining Animation */}
          <div className="mt-4 text-center ascii-art text-xs opacity-70">
            <pre className="inline-block">
{`    ${currentOre.ascii}
   /████\\
  /██████\\
 ▓▓▓▓▓▓▓▓▓▓`}
            </pre>
          </div>

          {/* Stop Button */}
          <button
            onClick={onStopMining}
            className="w-full mt-4 py-3 bg-red-600 hover:bg-red-700 text-white font-pixel text-xs rounded-lg transition-colors"
          >
            STOP MINING
          </button>
        </div>
      )}

      {/* Ore Selection */}
      <div className="space-y-3">
        <h2 className="font-pixel text-xs text-gray-400 uppercase tracking-wider">
          {isMining ? 'Other Ores' : 'Select Ore to Mine'}
        </h2>

        <div className="grid gap-3">
          {gameState.available_ores.map((ore) => (
            <OreCard
              key={ore.id}
              ore={ore}
              currentLevel={gameState.level}
              quantity={gameState.inventory[ore.id] || 0}
              isActive={ore.id === gameState.current_action}
              onSelect={() => onStartMining(ore.id)}
              disabled={isMining || !ore.unlocked}
            />
          ))}
        </div>
      </div>

      {/* Inventory Summary */}
      <div className="bg-[#16213e] rounded-xl p-4 border border-gray-700">
        <h3 className="font-pixel text-xs text-gray-400 mb-3">INVENTORY</h3>
        <div className="grid grid-cols-5 gap-2">
          {gameState.available_ores.map((ore) => (
            <div
              key={ore.id}
              className={`text-center p-2 rounded-lg ${
                ore.unlocked ? 'bg-[#1a1a2e]' : 'bg-[#1a1a2e] opacity-40'
              }`}
              title={ore.name}
            >
              <span className="font-pixel text-xs" style={{ color: ore.color }}>
                {ore.ascii}
              </span>
              <p className="text-xs text-gray-300 mt-1">
                {gameState.inventory[ore.id] || 0}
              </p>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}
