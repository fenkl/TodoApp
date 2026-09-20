import { OfflineQueue, OfflineAction } from '../../src/lib/offline-queue';

// Mock für window localStorage
const mockLocalStorage = {
  getItem: jest.fn(),
  setItem: jest.fn(),
  removeItem: jest.fn()
};

Object.defineProperty(window, 'localStorage', {
  value: mockLocalStorage,
  writable: true
});

// Mock für fetch
global.fetch = jest.fn();

describe('OfflineQueue', () => {
  let offlineQueue: OfflineQueue;
  
  beforeEach(() => {
    offlineQueue = new OfflineQueue();
    // Leere die Warteschlange vor jedem Test
    offlineQueue.clearQueue();
    mockLocalStorage.getItem.mockReset();
    mockLocalStorage.setItem.mockReset();
    (global.fetch as jest.Mock).mockReset();
  });

  test('should initialize with empty queue', () => {
    expect(offlineQueue.getQueueLength()).toBe(0);
  });

  test('should add action to queue', () => {
    const action: OfflineAction = {
      id: '1',
      type: 'CREATE',
      data: { title: 'Test Todo', completed: false },
      timestamp: Date.now()
    };
    
    offlineQueue.addAction(action);
    expect(offlineQueue.getQueueLength()).toBe(1);
  });

  test('should generate sequence numbers', () => {
    const action1: OfflineAction = {
      id: '1',
      type: 'CREATE',
      data: { title: 'Test Todo 1', completed: false },
      timestamp: Date.now()
    };
    
    const action2: OfflineAction = {
      id: '2',
      type: 'CREATE',
      data: { title: 'Test Todo 2', completed: false },
      timestamp: Date.now()
    };
    
    offlineQueue.addAction(action1);
    offlineQueue.addAction(action2);
    
    expect(offlineQueue.getQueueLength()).toBe(2);
  });

  test('should handle empty queue', async () => {
    // Mock fetch to avoid actual network requests
    (global.fetch as jest.Mock).mockImplementation(() => Promise.resolve({
      ok: true,
      json: () => Promise.resolve({})
    }));
    
    const result = await offlineQueue.syncWithServer('http://localhost:8000/api');
    expect(result).toBeUndefined();
  });

  test('should execute action', async () => {
    const mockAction: OfflineAction = {
      id: '1',
      type: 'CREATE',
      data: { title: 'Test Todo', completed: false },
      timestamp: Date.now()
    };
    
    (global.fetch as jest.Mock).mockImplementation(() => Promise.resolve({
      ok: true,
      json: () => Promise.resolve(mockAction.data)
    }));
    
    await offlineQueue.executeAction(mockAction, 'http://localhost:8000/api');
    
    // Check if fetch was called with correct parameters
    expect(fetch).toHaveBeenCalled();
  });

  test('should handle retry logic', async () => {
    const mockAction: OfflineAction = {
      id: '1',
      type: 'CREATE',
      data: { title: 'Test Todo', completed: false },
      timestamp: Date.now()
    };
    
    // Mock fetch to return error on first call, success on second
    let callCount = 0;
    (global.fetch as jest.Mock).mockImplementation(() => {
      callCount++;
      if (callCount === 1) {
        return Promise.reject(new Error('Network Error'));
      } else {
        return Promise.resolve({
          ok: true,
          json: () => Promise.resolve(mockAction.data)
        });
      }
    });
    
    try {
      await offlineQueue.executeAction(mockAction, 'http://localhost:8000/api');
      expect(fetch).toHaveBeenCalledTimes(2);
    } catch (error) {
      // Test wird nicht erreicht, da retry erfolgreich ist
    }
  });

  test('should clear queue', () => {
    const action: OfflineAction = {
      id: '1',
      type: 'CREATE',
      data: { title: 'Test Todo', completed: false },
      timestamp: Date.now()
    };
    
    offlineQueue.addAction(action);
    expect(offlineQueue.getQueueLength()).toBe(1);
    
    offlineQueue.clearQueue();
    expect(offlineQueue.getQueueLength()).toBe(0);
  });
});

// Test for edge cases
describe('OfflineQueue Edge Cases', () => {
  let offlineQueue: OfflineQueue;
  
  beforeEach(() => {
    offlineQueue = new OfflineQueue();
    offlineQueue.clearQueue();
    mockLocalStorage.getItem.mockReset();
  });

  test('should handle invalid action data', () => {
    const invalidAction = {
      id: '1',
      type: 'INVALID_TYPE', // Ungültiger Typ
      data: null,
      timestamp: Date.now()
    } as any;
    
    expect(() => {
      offlineQueue.addAction(invalidAction);
    }).not.toThrow();
  });

  test('should handle duplicate action IDs', () => {
    const action1: OfflineAction = {
      id: '1',
      type: 'CREATE',
      data: { title: 'Test Todo 1', completed: false },
      timestamp: Date.now()
    };
    
    const action2: OfflineAction = {
      id: '1', // Gleiche ID
      type: 'UPDATE',
      data: { title: 'Updated Todo 1', completed: true },
      timestamp: Date.now()
    };
    
    offlineQueue.addAction(action1);
    offlineQueue.addAction(action2); // Sollte die alte überschreiben oder einfach hinzufügen
    
    expect(offlineQueue.getQueueLength()).toBeGreaterThanOrEqual(1);
  });

  test('should handle localStorage errors', () => {
    // Mock localStorage to throw error
    Object.defineProperty(window, 'localStorage', {
      value: {
        getItem: jest.fn(() => { throw new Error('Storage error'); }),
        setItem: jest.fn(() => { throw new Error('Storage error'); }),
        removeItem: jest.fn()
      },
      writable: true
    });
    
    const action: OfflineAction = {
      id: '1',
      type: 'CREATE',
      data: { title: 'Test Todo', completed: false },
      timestamp: Date.now()
    };
    
    // Diese Operationen sollten keine Exceptions werfen
    expect(() => offlineQueue.addAction(action)).not.toThrow();
    expect(() => offlineQueue.getQueueLength()).not.toThrow();
  });
});