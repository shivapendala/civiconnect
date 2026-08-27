import 'package:flutter/material.dart';

class NotificationPreferencesScreen extends StatefulWidget {
  const NotificationPreferencesScreen({super.key});

  @override
  State<NotificationPreferencesScreen> createState() => _NotificationPreferencesScreenState();
}

class _NotificationPreferencesScreenState extends State<NotificationPreferencesScreen> {
  bool _pushEnabled = true;
  bool _emailEnabled = true;
  bool _smsEnabled = false;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Notification Preferences'),
      ),
      body: ListView(
        padding: const EdgeInsets.all(16.0),
        children: [
          const Text('Choose how you want to be notified about updates to your complaints and assignments.', 
            style: TextStyle(color: Colors.grey)),
          const SizedBox(height: 24),
          SwitchListTile(
            title: const Text('Push Notifications'),
            subtitle: const Text('Receive alerts directly on your device.'),
            value: _pushEnabled,
            onChanged: (val) => setState(() => _pushEnabled = val),
            secondary: const Icon(Icons.touch_app, color: Colors.blue),
          ),
          const Divider(),
          SwitchListTile(
            title: const Text('Email Notifications'),
            subtitle: const Text('Receive detailed updates in your inbox.'),
            value: _emailEnabled,
            onChanged: (val) => setState(() => _emailEnabled = val),
            secondary: const Icon(Icons.email, color: Colors.orange),
          ),
          const Divider(),
          SwitchListTile(
            title: const Text('SMS Notifications'),
            subtitle: const Text('Receive text messages for critical alerts (Standard rates apply).'),
            value: _smsEnabled,
            onChanged: (val) => setState(() => _smsEnabled = val),
            secondary: const Icon(Icons.sms, color: Colors.green),
          ),
          const SizedBox(height: 32),
          ElevatedButton(
            onPressed: () {
              ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text('Preferences saved successfully')));
              Navigator.pop(context);
            },
            child: const Padding(
              padding: EdgeInsets.all(12.0),
              child: Text('Save Preferences', style: TextStyle(fontSize: 16)),
            ),
          )
        ],
      ),
    );
  }
}
