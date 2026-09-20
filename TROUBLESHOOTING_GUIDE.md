# TodoSync Troubleshooting Guide

## Overview

This guide provides solutions for common issues and problems encountered when using the TodoSync application across different platforms and deployment scenarios.

## Common Issues and Solutions

### 1. Connection Problems

#### Issue: Cannot connect to backend server
**Symptoms:**
- "Connection failed" or "Server not responding" errors
- Applications cannot synchronize todos
- Offline mode activated immediately

**Solutions:**
1. **Verify Server Accessibility:**
   ```bash
   # Test connectivity from client device
   ping 192.168.2.2
   telnet 192.168.2.2 8000
   ```

2. **Check Backend Service Status:**
   ```bash
   # On Raspberry Pi or server
   sudo systemctl status todosync-backend.service
   ```

3. **Verify Network Configuration:**
   - Ensure both devices are on the same LAN network
   - Check firewall settings allow connections on port 8000
   - Verify IP address is correct in client configuration

#### Issue: WebSocket connection fails
**Symptoms:**
- GUI updates not happening in real-time
- "WebSocket disconnected" messages
- Synchronization delays

**Solutions:**
1. **Check Network Connectivity:**
   ```bash
   # Test if WebSocket endpoint is accessible
   curl -i -N -H "Connection: upgrade" -H "Upgrade: websocket" http://192.168.2.2:8000/ws/1
   ```

2. **Verify Server Port:**
   ```bash
   # Check if port 8000 is listening
   netstat -tuln | grep :8000
   ss -tuln | grep :8000
   ```

3. **Browser/Client Issues:**
   - Clear browser cache and cookies
   - Try different browser or client application version

### 2. Synchronization Problems

#### Issue: Todos not syncing between devices
**Symptoms:**
- Changes made on one device don't appear on others
- Manual refresh required to see updates  
- Conflicts reported but not resolved

**Solutions:**
1. **Check Sequence Numbers:**
   ```bash
   # Verify database sequence numbers
   sqlite3 backend/todos.db "SELECT id, title, sequence_number FROM todos ORDER BY id;"
   ```

2. **Clear Offline Queue:**
   - Restart application to clear local queue
   - Manually clear localStorage in browser developer tools

3. **Verify Conflict Resolution:**
   ```bash
   # Check conflict logs  
   curl http://192.168.2.2:8000/api/v1/conflict-logs
   ```

#### Issue: Conflict resolution not working properly
**Symptoms:**
- "Last Write Wins" logic doesn't determine the correct winner
- Conflicts still appear after sync operation
- Incorrect todos displayed in GUI

**Solutions:**
1. **Debug Sequence Numbers:**
   - Check that sequence numbers are incrementing correctly
   - Verify that higher sequence number wins in conflicts

2. **Database Schema Verification:**
   ```sql
   -- In SQLite database
   PRAGMA table_info(todos);
   PRAGMA table_info(conflict_logs);
   ```

3. **Review Conflict Handler Code:**
   - Ensure no eval() usage is present (was replaced with JSON parsing)
   - Verify LWW resolution logic in backend/conflict_handler.py

### 3. Mobile Application Issues

#### Issue: Android app crashes on startup
**Symptoms:**
- App closes immediately upon launch
- "Unfortunately, TodoSync has stopped" message
- No error logs visible

**Solutions:**
1. **Verify Android Build Requirements:**
   - Ensure ADB is properly configured
   - Check target Android API level compatibility
   - Verify device has sufficient storage and permissions

2. **Debug with Logs:**
   ```bash
   # View Android logs  
   adb logcat | grep TodoSync
   ```

3. **Check Tauri Configuration:**
   ```bash
   # Ensure tauri.conf.json is properly configured for Android
   cat tauri.conf.json
   ```

#### Issue: App not displaying notifications
**Symptoms:**
- No push notifications even when enabled
- Notification settings don't save preferences
- Desktop notifications work but mobile doesn't

**Solutions:**
1. **Request Permissions:**
   - Ensure user grants notification permissions through app UI
   - Verify system-level notification permissions are enabled

2. **Check Platform Support:**
   ```bash
   # Validate notification configuration in Rust code
   cat src-tauri/src/notification.rs
   ```

### 4. Performance Issues

#### Issue: Slow synchronization or application lag
**Symptoms:**
- Long delays between operations and updates  
- App becomes unresponsive during sync
- High CPU usage on client devices

**Solutions:**
1. **Optimize Database Query:**
   ```bash
   # Analyze database performance
   sqlite3 backend/todos.db "EXPLAIN QUERY PLAN SELECT * FROM todos;"
   ```

2. **Check Network Bandwidth:**
   - Monitor network traffic between devices
   - Ensure adequate bandwidth for sync operations

3. **Reduce Offline Queue Size:**
   - Clear old entries if queue becomes too large
   - Implement batch processing for large update sets

### 5. Database Issues

#### Issue: Corrupted database or data loss
**Symptoms:**
- Application crash on startup due to database issues
- Lost todos or inconsistent data
- Error messages like "database is locked"

**Solutions:**
1. **Database Recovery:**
   ```bash
   # Create backup before recovery
   cp backend/todos.db backend/todos.db.backup
   
   # Check for consistency
   sqlite3 backend/todos.db ".schema"
   ```

2. **Manual Database Repair:**
   - Delete corrupted database file and reinitialize 
   - Restore from backup if available

3. **Verify Transactions:**
   ```sql
   -- Ensure transactions are working properly  
   PRAGMA synchronous;
   PRAGMA journal_mode;
   ```

### 6. Development Environment Issues

#### Issue: Build failures during compilation
**Symptoms:**
- "Cannot find module" errors
- "Build failed" messages when running Tauri commands
- Dependency resolution issues with npm or cargo

**Solutions:**
1. **Clean and Rebuild:**
   ```bash
   # Clean npm cache
   npm cache clean --force
   
   # Clear node_modules and reinstall
   rm -rf node_modules
   npm install
   ```

2. **Rust Environment Check:**
   ```bash
   # Update rust toolchain
   rustup update
   
   # Verify Tauri dependencies
   cargo check
   ```

3. **Verify System Requirements:**
   - Ensure correct Node.js version (16+)
   - Confirm Rust is installed correctly with Tauri support
   - Check Android SDK paths are configured correctly

## Advanced Debugging Techniques

### 1. Logging Analysis
Enable detailed logging by:
```bash
# Set environment variables for debugging
export TODO_DEBUG=1
export TODO_LOG_LEVEL=DEBUG
```

### 2. Network Monitoring
Use tools to track network activity:
```bash
# Monitor connections to backend
tcpdump -i any port 8000
wireshark -i eth0 -f "tcp port 8000"
```

### 3. Memory Usage Analysis
Monitor application performance:
```bash
# Check memory usage
top
htop
ps aux | grep todosync
```

## Known Issues and Workarounds

### Issue: Race Condition in Concurrent Writes
- **Problem:** Simultaneous writes can cause conflicts or data loss
- **Workaround:** Backend uses database transactions for atomic operations
- **Resolution:** Sequence number tracking ensures proper ordering

### Issue: Offline Queue Persistence
- **Problem:** Queue may not persist between app sessions on some platforms  
- **Workaround:** Implementation uses localStorage with error handling
- **Resolution:** Retry logic with exponential backoff implemented

### Issue: Browser Compatibility
- **Problem:** Some older browsers may not support WebSocket or localStorage
- **Workaround:** Modern browser requirements specified in documentation
- **Resolution:** Progressive enhancement approach with fallbacks

## When to Seek Help

If you encounter issues not covered by this guide:

1. **Check Documentation:** Review all relevant documentation sections
2. **Search Issues:** Look for similar problems in issue trackers
3. **Contact Support:** Report bugs through official channels with:
   - System information (OS, hardware specs)
   - Error messages and logs  
   - Steps to reproduce the issue
4. **Community Forums:** Post questions on relevant developer forums

## Prevention Best Practices

1. **Regular Updates:** Keep all components updated regularly
2. **Backups:** Maintain regular backups of configuration and data
3. **Monitoring:** Implement monitoring for production environments
4. **Testing:** Test deployment scenarios before production rollout
5. **Documentation:** Maintain updated records of your specific setup

## Support Resources

- **Official Documentation:** https://github.com/todosync/docs
- **GitHub Repository:** https://github.com/todosync/todoapp
- **Issue Tracker:** https://github.com/todosync/todoapp/issues
- **Community Forum:** https://todosync.discussion.com