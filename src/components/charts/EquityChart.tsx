import React, { useEffect, useRef } from 'react';
import { createChart, ColorType, IChartApi, ISeriesApi } from 'lightweight-charts';

interface EquityPoint {
  date: string;
  equity: number;
  profitLoss: number;
  profitLossPct: number;
}

interface EquityChartProps {
  data: EquityPoint[];
  height?: number;
}

const EquityChart: React.FC<EquityChartProps> = ({ data, height = 400 }) => {
  const chartContainerRef = useRef<HTMLDivElement>(null);
  const chartRef = useRef<IChartApi | null>(null);
  const seriesRef = useRef<ISeriesApi<'Line'> | null>(null);

  useEffect(() => {
    if (!chartContainerRef.current) return;

    // Create chart
    const chart = createChart(chartContainerRef.current, {
      layout: {
        background: { type: ColorType.Solid, color: '#ffffff' },
        textColor: '#333',
      },
      width: chartContainerRef.current.clientWidth,
      height: height,
      grid: {
        vertLines: { color: '#f0f0f0' },
        horzLines: { color: '#f0f0f0' },
      },
      rightPriceScale: {
        borderColor: '#e5e7eb',
      },
      timeScale: {
        borderColor: '#e5e7eb',
        timeVisible: true,
      },
    });

    // Add line series
    const lineSeries = chart.addLineSeries({
      color: '#3b82f6',
      lineWidth: 2,
      priceFormat: {
        type: 'price',
        precision: 2,
        minMove: 0.01,
      },
    });

    chartRef.current = chart;
    seriesRef.current = lineSeries;

    // Handle resize
    const handleResize = () => {
      if (chartContainerRef.current && chartRef.current) {
        chartRef.current.applyOptions({
          width: chartContainerRef.current.clientWidth,
        });
      }
    };

    window.addEventListener('resize', handleResize);

    return () => {
      window.removeEventListener('resize', handleResize);
      chart.remove();
    };
  }, [height]);

  useEffect(() => {
    if (!seriesRef.current || !data || data.length === 0) return;

    // Convert data to chart format
    const chartData = data.map((point) => ({
      time: new Date(point.date).getTime() / 1000, // Convert to UNIX timestamp
      value: point.equity,
    }));

    seriesRef.current.setData(chartData);

    // Fit content
    if (chartRef.current) {
      chartRef.current.timeScale().fitContent();
    }
  }, [data]);

  return (
    <div>
      <div ref={chartContainerRef} style={{ position: 'relative' }} />
    </div>
  );
};

export default EquityChart;
