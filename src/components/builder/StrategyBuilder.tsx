import React, { useState } from 'react';
import './StrategyBuilder.css';

interface Block {
  id: string;
  type: 'trigger' | 'condition' | 'action' | 'universe';
  label: string;
  config: any;
}

const StrategyBuilder: React.FC = () => {
  const [blocks, setBlocks] = useState<Block[]>([]);
  const [selectedBlock, setSelectedBlock] = useState<Block | null>(null);

  const blockPalette = [
    // Triggers
    { type: 'trigger', category: 'Triggers', items: [
      { id: 'time-interval', label: 'Time Interval', icon: '⏰' },
      { id: 'market-open', label: 'Market Open', icon: '🔔' },
      { id: 'market-close', label: 'Market Close', icon: '🔕' },
      { id: 'price-alert', label: 'Price Alert', icon: '📊' },
    ]},
    // Universe
    { type: 'universe', category: 'Universe', items: [
      { id: 'watchlist', label: 'Watchlist', icon: '👁️' },
      { id: 'sp500', label: 'S&P 500', icon: '📈' },
      { id: 'nasdaq100', label: 'NASDAQ 100', icon: '💻' },
      { id: 'custom', label: 'Custom List', icon: '📝' },
    ]},
    // Conditions
    { type: 'condition', category: 'Conditions', items: [
      { id: 'price-vs-ma', label: 'Price vs MA', icon: '📊' },
      { id: 'rsi-level', label: 'RSI Level', icon: '📉' },
      { id: 'macd-cross', label: 'MACD Cross', icon: '〰️' },
      { id: 'volume-spike', label: 'Volume Spike', icon: '📊' },
      { id: 'bollinger', label: 'Bollinger Bands', icon: '📊' },
    ]},
    // Actions
    { type: 'action', category: 'Actions', items: [
      { id: 'buy', label: 'Buy', icon: '📈' },
      { id: 'sell', label: 'Sell', icon: '📉' },
      { id: 'set-stop', label: 'Set Stop Loss', icon: '🛑' },
      { id: 'set-target', label: 'Set Target', icon: '🎯' },
      { id: 'notify', label: 'Send Alert', icon: '🔔' },
    ]},
  ];

  const addBlock = (blockType: string, blockId: string, label: string) => {
    const newBlock: Block = {
      id: `${blockId}-${Date.now()}`,
      type: blockType as any,
      label,
      config: {},
    };
    setBlocks([...blocks, newBlock]);
  };

  const removeBlock = (id: string) => {
    setBlocks(blocks.filter(b => b.id !== id));
    if (selectedBlock?.id === id) {
      setSelectedBlock(null);
    }
  };

  const generateStrategy = () => {
    // Convert blocks to strategy configuration
    const strategyConfig = {
      name: 'Custom Strategy',
      blocks: blocks.map(b => ({
        type: b.type,
        id: b.id,
        label: b.label,
        config: b.config,
      })),
    };

    console.log('Generated Strategy:', strategyConfig);
    alert('Strategy configuration generated! Check console for details.');
  };

  return (
    <div className="strategy-builder">
      <div className="builder-header">
        <h2>🔧 Visual Strategy Builder</h2>
        <p>Create custom strategies with drag-and-drop blocks</p>
      </div>

      <div className="builder-container">
        {/* Block Palette */}
        <div className="block-palette">
          <h3>Block Palette</h3>
          {blockPalette.map((category) => (
            <div key={category.category} className="palette-category">
              <div className="category-header">{category.category}</div>
              <div className="category-items">
                {category.items.map((item) => (
                  <div
                    key={item.id}
                    className="palette-block"
                    onClick={() => addBlock(category.type, item.id, item.label)}
                  >
                    <span className="block-icon">{item.icon}</span>
                    <span className="block-label">{item.label}</span>
                  </div>
                ))}
              </div>
            </div>
          ))}
        </div>

        {/* Canvas */}
        <div className="builder-canvas">
          <div className="canvas-header">
            <h3>Strategy Flow</h3>
            {blocks.length > 0 && (
              <button className="btn btn-primary" onClick={generateStrategy}>
                Generate Strategy
              </button>
            )}
          </div>

          {blocks.length === 0 ? (
            <div className="empty-canvas">
              <p>👈 Click blocks from the palette to start building your strategy</p>
            </div>
          ) : (
            <div className="canvas-blocks">
              {blocks.map((block, index) => (
                <div key={block.id} className="canvas-block-wrapper">
                  <div
                    className={`canvas-block ${block.type} ${selectedBlock?.id === block.id ? 'selected' : ''}`}
                    onClick={() => setSelectedBlock(block)}
                  >
                    <div className="block-header">
                      <span className="block-type-label">{block.type}</span>
                      <button
                        className="remove-block"
                        onClick={(e) => {
                          e.stopPropagation();
                          removeBlock(block.id);
                        }}
                      >
                        ✕
                      </button>
                    </div>
                    <div className="block-content">
                      <div className="block-label">{block.label}</div>
                    </div>
                  </div>
                  {index < blocks.length - 1 && (
                    <div className="block-connector">↓</div>
                  )}
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Configuration Panel */}
        <div className="config-panel">
          <h3>Configuration</h3>
          {selectedBlock ? (
            <div className="block-config">
              <div className="config-header">
                <strong>{selectedBlock.label}</strong>
              </div>
              <div className="config-body">
                <p className="config-hint">
                  Configuration options for {selectedBlock.label} would appear here.
                </p>
                {selectedBlock.type === 'trigger' && selectedBlock.id.includes('time-interval') && (
                  <div className="form-group">
                    <label>Interval</label>
                    <select className="input">
                      <option value="1min">Every 1 minute</option>
                      <option value="5min">Every 5 minutes</option>
                      <option value="15min">Every 15 minutes</option>
                      <option value="1hour">Every hour</option>
                    </select>
                  </div>
                )}
                {selectedBlock.type === 'universe' && (
                  <div className="form-group">
                    <label>Symbols</label>
                    <input
                      type="text"
                      className="input"
                      placeholder="AAPL, MSFT, GOOGL"
                    />
                  </div>
                )}
                {selectedBlock.type === 'condition' && selectedBlock.id.includes('rsi') && (
                  <>
                    <div className="form-group">
                      <label>RSI Period</label>
                      <input type="number" className="input" defaultValue={14} />
                    </div>
                    <div className="form-group">
                      <label>Threshold</label>
                      <select className="input">
                        <option value="oversold">Oversold (&lt; 30)</option>
                        <option value="overbought">Overbought (&gt; 70)</option>
                      </select>
                    </div>
                  </>
                )}
                {selectedBlock.type === 'action' && selectedBlock.id.includes('buy') && (
                  <>
                    <div className="form-group">
                      <label>Order Type</label>
                      <select className="input">
                        <option value="market">Market</option>
                        <option value="limit">Limit</option>
                      </select>
                    </div>
                    <div className="form-group">
                      <label>Position Size</label>
                      <input type="number" className="input" defaultValue={10} />
                      <span className="input-suffix">% of portfolio</span>
                    </div>
                  </>
                )}
              </div>
            </div>
          ) : (
            <div className="no-selection">
              <p>Select a block to configure it</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default StrategyBuilder;
