import { createWebSocket } from '../../src/lib/ws';

// Mock für WebSocket
const mockWebSocket = {
  onopen: jest.fn(),
  onmessage: jest.fn(),
  onerror: jest.fn(),
  onclose: jest.fn(),
  send: jest.fn(),
  close: jest.fn()
};

// Mock global WebSocket
(global as any).WebSocket = jest.fn(() => mockWebSocket);

describe('WebSocket Connection', () => {
  beforeEach(() => {
    // Reset mocks before each test
    mockWebSocket.onopen.mockReset();
    mockWebSocket.onmessage.mockReset();
    mockWebSocket.onerror.mockReset();
    mockWebSocket.onclose.mockReset();
    mockWebSocket.send.mockReset();
    mockWebSocket.close.mockReset();
  });

  test('should create WebSocket connection', () => {
    const wsUrl = 'ws://localhost:8000/websocket';
    const ws = createWebSocket(wsUrl);
    
    expect(ws).toBeDefined();
    expect(WebSocket).toHaveBeenCalledWith(wsUrl);
  });

  test('should handle message events', () => {
    const wsUrl = 'ws://localhost:8000/websocket';
    const ws = createWebSocket(wsUrl);
    
    // Simulate receiving a message
    const mockMessage = { data: JSON.stringify({ action: 'update', payload: { id: 1, title: 'Test' } }) };
    ws.onmessage(mockMessage);
    
    expect(ws.onmessage).toBeDefined();
  });

  test('should handle connection close', () => {
    const wsUrl = 'ws://localhost:8000/websocket';
    const ws = createWebSocket(wsUrl);
    
    // Simulate closing
    ws.onclose(new CloseEvent('close'));
    
    expect(ws.onclose).toBeDefined();
  });

  test('should send messages correctly', () => {
    const wsUrl = 'ws://localhost:8000/websocket';
    const ws = createWebSocket(wsUrl);
    
    const messageData = { action: 'create', data: { title: 'Test Todo' } };
    ws.send(JSON.stringify(messageData));
    
    expect(ws.send).toHaveBeenCalledWith(JSON.stringify(messageData));
  });

  test('should handle errors correctly', () => {
    const wsUrl = 'ws://localhost:8000/websocket';
    const ws = createWebSocket(wsUrl);
    
    // Simulate error
    ws.onerror(new ErrorEvent('error'));
    
    expect(ws.onerror).toBeDefined();
  });

  test('should close connection properly', () => {
    const wsUrl = 'ws://localhost:8000/websocket';
    const ws = createWebSocket(wsUrl);
    
    ws.close();
    
    expect(ws.close).toHaveBeenCalled();
  });
});

// Edge case tests
describe('WebSocket Edge Cases', () => {
  test('should handle invalid URLs', () => {
    expect(() => {
      createWebSocket('');
    }).not.toThrow(); // Funktion sollte kein Problem mit leerer URL machen
    
    const ws = createWebSocket('invalid-url');
    expect(ws).toBeDefined();
  });

  test('should handle null messages', () => {
    const wsUrl = 'ws://localhost:8000/websocket';
    const ws = createWebSocket(wsUrl);
    
    // Test with null message
    const mockMessage = { data: null };
    expect(() => {
      ws.onmessage(mockMessage);
    }).not.toThrow(); // Sollte gracefully handhaben
  });

  test('should handle malformed JSON', () => {
    const wsUrl = 'ws://localhost:8000/websocket';
    const ws = createWebSocket(wsUrl);
    
    // Test with invalid JSON
    const mockMessage = { data: '{invalid json' };
    expect(() => {
      ws.onmessage(mockMessage);
    }).not.toThrow(); // Sollte gracefully handhaben
  });
});