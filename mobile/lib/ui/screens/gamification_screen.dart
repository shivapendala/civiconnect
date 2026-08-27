import 'package:flutter/material.dart';

class GamificationScreen extends StatelessWidget {
  const GamificationScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Civic Engagement')),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            _buildProfileCard(),
            const SizedBox(height: 24),
            _buildBadgesSection(),
            const SizedBox(height: 24),
            _buildLeaderboardSection(),
          ],
        ),
      ),
    );
  }

  Widget _buildProfileCard() {
    return Card(
      elevation: 4,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
      child: Container(
        decoration: BoxDecoration(
          borderRadius: BorderRadius.circular(16),
          gradient: LinearGradient(
            colors: [Colors.blue.shade700, Colors.blue.shade500],
            begin: Alignment.topLeft,
            end: Alignment.bottomRight,
          ),
        ),
        padding: const EdgeInsets.all(24.0),
        child: Column(
          children: [
            const CircleAvatar(
              radius: 40,
              backgroundColor: Colors.white,
              child: Icon(Icons.person, size: 40, color: Colors.blue),
            ),
            const SizedBox(height: 16),
            const Text(
              'Level 5 Civic Leader',
              style: TextStyle(color: Colors.white, fontSize: 24, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 8),
            const Text(
              '450 Points',
              style: TextStyle(color: Colors.white70, fontSize: 18),
            ),
            const SizedBox(height: 16),
            LinearProgressIndicator(
              value: 0.5,
              backgroundColor: Colors.white24,
              valueColor: const AlwaysStoppedAnimation<Color>(Colors.white),
              borderRadius: BorderRadius.circular(4),
            ),
            const SizedBox(height: 8),
            const Text('50 pts to Level 6', style: TextStyle(color: Colors.white70)),
          ],
        ),
      ),
    );
  }

  Widget _buildBadgesSection() {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        const Text('Your Badges', style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold)),
        const SizedBox(height: 16),
        Row(
          mainAxisAlignment: MainAxisAlignment.spaceAround,
          children: [
            _buildBadge('First Reporter', Icons.flag, Colors.orange),
            _buildBadge('Community Hero', Icons.shield, Colors.red),
            _buildBadge('Eco Warrior', Icons.eco, Colors.green),
          ],
        )
      ],
    );
  }

  Widget _buildBadge(String name, IconData icon, Color color) {
    return Column(
      children: [
        CircleAvatar(
          radius: 30,
          backgroundColor: color.withOpacity(0.2),
          child: Icon(icon, size: 30, color: color),
        ),
        const SizedBox(height: 8),
        Text(name, style: const TextStyle(fontWeight: FontWeight.bold)),
      ],
    );
  }

  Widget _buildLeaderboardSection() {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        const Text('Leaderboard', style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold)),
        const SizedBox(height: 16),
        Card(
          elevation: 2,
          child: Column(
            children: [
              _buildLeaderboardRow(1, 'Jane Doe', '1,200', isMe: false),
              const Divider(height: 1),
              _buildLeaderboardRow(2, 'John Smith', '950', isMe: false),
              const Divider(height: 1),
              _buildLeaderboardRow(3, 'You', '450', isMe: true),
              const Divider(height: 1),
              _buildLeaderboardRow(4, 'Alex A', '420', isMe: false),
            ],
          ),
        ),
      ],
    );
  }

  Widget _buildLeaderboardRow(int rank, String name, String points, {bool isMe = false}) {
    return ListTile(
      tileColor: isMe ? Colors.blue.shade50 : null,
      leading: CircleAvatar(
        backgroundColor: rank == 1 ? Colors.amber : (rank == 2 ? Colors.grey.shade400 : (rank == 3 ? Colors.brown.shade300 : Colors.blue.shade100)),
        child: Text('#$rank', style: const TextStyle(color: Colors.black87, fontWeight: FontWeight.bold)),
      ),
      title: Text(name, style: TextStyle(fontWeight: isMe ? FontWeight.bold : FontWeight.normal)),
      trailing: Text('$points pts', style: const TextStyle(fontWeight: FontWeight.bold, color: Colors.blue)),
    );
  }
}
