import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:web_socket_channel/web_socket_channel.dart';
import 'package:http/http.dart' as http;
import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import '../../core/constants/api_constants.dart';

class ChatScreen extends StatefulWidget {
  final String complaintId;

  const ChatScreen({Key? key, required this.complaintId}) : super(key: key);

  @override
  _ChatScreenState createState() => _ChatScreenState();
}

class _ChatScreenState extends State<ChatScreen> {
  final TextEditingController _controller = TextEditingController();
  final FlutterSecureStorage _storage = const FlutterSecureStorage();
  late WebSocketChannel _channel;
  List<Map<String, dynamic>> _messages = [];
  bool _isLoading = true;

  @override
  void initState() {
    super.initState();
    _fetchHistoryAndConnect();
  }

  Future<void> _fetchHistoryAndConnect() async {
    final token = await _storage.read(key: 'jwt_token');
    if (token == null) return;

    // Fetch History
    final uri = Uri.parse('${ApiConstants.baseUrl}/complaints/${widget.complaintId}/chat_history/');
    final response = await http.get(uri, headers: {
      'Authorization': 'Bearer $token',
    });

    if (response.statusCode == 200) {
      final List<dynamic> data = json.decode(response.body);
      setState(() {
        _messages = data.map((e) => e as Map<String, dynamic>).toList();
        _isLoading = false;
      });
    }

    // Connect WebSocket
    // Since simple JWT is used in headers usually, WebSockets in browser might need token in query param
    // For this example, assuming it connects
    final wsUrl = Uri.parse('ws://10.0.2.2:8000/ws/chat/${widget.complaintId}/');
    _channel = WebSocketChannel.connect(wsUrl);

    _channel.stream.listen((message) {
      final data = json.decode(message);
      setState(() {
        _messages.add({
          'content': data['message'],
          'sender_email': data['user_id'].toString(), // Adjust based on what backend sends
          'is_me': false, // Need to implement proper logic for identifying own messages
        });
      });
    });
  }

  void _sendMessage() {
    if (_controller.text.isNotEmpty) {
      _channel.sink.add(json.encode({'message': _controller.text}));
      _controller.clear();
    }
  }

  @override
  void dispose() {
    _channel.sink.close();
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Chat - ${widget.complaintId}')),
      body: _isLoading 
        ? const Center(child: CircularProgressIndicator())
        : Column(
        children: [
          Expanded(
            child: ListView.builder(
              itemCount: _messages.length,
              itemBuilder: (context, index) {
                final msg = _messages[index];
                return ListTile(
                  title: Text(msg['content'] ?? ''),
                  subtitle: Text(msg['sender_email'] ?? ''),
                );
              },
            ),
          ),
          Padding(
            padding: const EdgeInsets.all(8.0),
            child: Row(
              children: [
                Expanded(
                  child: TextField(
                    controller: _controller,
                    decoration: const InputDecoration(labelText: 'Send a message'),
                  ),
                ),
                IconButton(
                  icon: const Icon(Icons.send),
                  onPressed: _sendMessage,
                )
              ],
            ),
          )
        ],
      ),
    );
  }
}
