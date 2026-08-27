import 'dart:convert';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:dio/dio.dart';
import 'api_service.dart';

class OfflineSyncManager {
  static const String _syncQueueKey = 'offline_sync_queue';
  final ApiService _apiService = ApiService();

  Future<void> queueOfflineAction(String endpoint, String method, Map<String, dynamic> data) async {
    final prefs = await SharedPreferences.getInstance();
    
    List<String> currentQueue = prefs.getStringList(_syncQueueKey) ?? [];
    
    final action = {
      'endpoint': endpoint,
      'method': method,
      'data': data,
      'timestamp': DateTime.now().toIso8601String(),
    };
    
    currentQueue.add(jsonEncode(action));
    await prefs.setStringList(_syncQueueKey, currentQueue);
  }

  Future<void> syncOfflineData() async {
    final prefs = await SharedPreferences.getInstance();
    List<String> currentQueue = prefs.getStringList(_syncQueueKey) ?? [];
    
    if (currentQueue.isEmpty) return;

    List<String> remainingQueue = [];

    for (String actionStr in currentQueue) {
      final action = jsonDecode(actionStr);
      try {
        if (action['method'] == 'POST') {
          await _apiService.dio.post(action['endpoint'], data: action['data']);
        } else if (action['method'] == 'PUT') {
          await _apiService.dio.put(action['endpoint'], data: action['data']);
        }
      } catch (e) {
        // If it fails due to network, keep it in the queue
        remainingQueue.add(actionStr);
      }
    }

    await prefs.setStringList(_syncQueueKey, remainingQueue);
  }

  // --- Caching for Offline Reads ---

  Future<void> cacheData(String key, dynamic data) async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString('cache_$key', jsonEncode(data));
  }

  Future<dynamic> getCachedData(String key) async {
    final prefs = await SharedPreferences.getInstance();
    final dataStr = prefs.getString('cache_$key');
    if (dataStr != null) {
      return jsonDecode(dataStr);
    }
    return null;
  }
}
