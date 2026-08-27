import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';

class HomeScreen extends StatelessWidget {
  const HomeScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Citizen Dashboard'),
        actions: [
          IconButton(
            icon: const Icon(Icons.person),
            onPressed: () {}, // Navigate to profile
          )
        ],
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Summary Header
            Text(
              'My Complaints',
              style: Theme.of(context).textTheme.titleLarge?.copyWith(fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 16),
            
            // Status Cards
            Row(
              children: [
                Expanded(child: _buildStatusCard(context, 'Pending', '2', Colors.orange)),
                const SizedBox(width: 8),
                Expanded(child: _buildStatusCard(context, 'In Progress', '1', Colors.blue)),
                const SizedBox(width: 8),
                Expanded(child: _buildStatusCard(context, 'Resolved', '5', Colors.green)),
              ],
            ),
            const SizedBox(height: 32),

            // Quick Actions
            Text(
              'Quick Actions',
              style: Theme.of(context).textTheme.titleLarge?.copyWith(fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 16),
            GridView.count(
              crossAxisCount: 2,
              shrinkWrap: true,
              physics: const NeverScrollableScrollPhysics(),
              crossAxisSpacing: 16,
              mainAxisSpacing: 16,
              childAspectRatio: 1.5,
              children: [
                _buildActionCard(context, 'Report Problem', Icons.add_circle, Colors.blue, onTap: () => context.push('/report')),
                _buildActionCard(context, 'Nearby Problems', Icons.location_on, Colors.red, onTap: () => context.push('/citizen_map')),
                _buildActionCard(context, 'My Complaints', Icons.list_alt, Colors.purple, onTap: () {}),
                _buildActionCard(context, 'Notifications', Icons.notifications, Colors.orange, onTap: () {}),
              ],
            ),
            const SizedBox(height: 32),
            
            // Nearby Issues Section
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Text(
                  'Nearby Issues',
                  style: Theme.of(context).textTheme.titleLarge?.copyWith(fontWeight: FontWeight.bold),
                ),
                TextButton(onPressed: (){}, child: const Text('See All'))
              ],
            ),
            const SizedBox(height: 16),
            _buildNearbyIssueTile(context, 'Pothole on Main St', 'Pending', '1.2 km away'),
            _buildNearbyIssueTile(context, 'Broken Streetlight', 'In Progress', '2.5 km away'),
          ],
        ),
      ),
      floatingActionButton: FloatingActionButton.extended(
        onPressed: () => context.push('/report'),
        icon: const Icon(Icons.add),
        label: const Text('Report'),
      ),
    );
  }

  Widget _buildStatusCard(BuildContext context, String title, String count, Color color) {
    return Card(
      elevation: 2,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
      child: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          children: [
            Text(
              count,
              style: Theme.of(context).textTheme.headlineMedium?.copyWith(
                color: color,
                fontWeight: FontWeight.bold,
              ),
            ),
            const SizedBox(height: 8),
            Text(
              title,
              style: Theme.of(context).textTheme.bodySmall,
              textAlign: TextAlign.center,
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildActionCard(BuildContext context, String title, IconData icon, Color color, {required VoidCallback onTap}) {
    return InkWell(
      onTap: onTap,
      borderRadius: BorderRadius.circular(12),
      child: Card(
        elevation: 2,
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(icon, size: 32, color: color),
            const SizedBox(height: 8),
            Text(title, style: Theme.of(context).textTheme.bodyMedium, textAlign: TextAlign.center),
          ],
        ),
      ),
    );
  }

  Widget _buildNearbyIssueTile(BuildContext context, String title, String status, String distance) {
    return Card(
      margin: const EdgeInsets.only(bottom: 12),
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
      child: ListTile(
        leading: const CircleAvatar(
          backgroundColor: Colors.blueAccent,
          child: Icon(Icons.report_problem, color: Colors.white),
        ),
        title: Text(title, style: const TextStyle(fontWeight: FontWeight.bold)),
        subtitle: Text('$status • $distance'),
        trailing: const Icon(Icons.chevron_right),
        onTap: () => context.push('/complaint/CC-2026-00001245'),
      ),
    );
  }
}
