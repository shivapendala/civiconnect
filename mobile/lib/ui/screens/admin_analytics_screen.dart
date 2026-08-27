import 'package:flutter/material.dart';
import 'package:fl_chart/fl_chart.dart';

class AdminAnalyticsScreen extends StatelessWidget {
  const AdminAnalyticsScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('City Analytics'),
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            _buildStatCards(),
            const SizedBox(height: 24),
            const Text('Complaint Distribution', style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold)),
            const SizedBox(height: 16),
            _buildCategoryPieChart(),
            const SizedBox(height: 32),
            const Text('Department Workload', style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold)),
            const SizedBox(height: 16),
            _buildDepartmentBarChart(),
            const SizedBox(height: 32),
            const Text('Performance & Citizen Satisfaction', style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold)),
            const SizedBox(height: 16),
            _buildPerformanceMetrics(),
          ],
        ),
      ),
    );
  }

  Widget _buildStatCards() {
    return Row(
      children: [
        Expanded(child: _buildSingleStatCard('Total Complaints', '1,245', Colors.blue)),
        const SizedBox(width: 12),
        Expanded(child: _buildSingleStatCard('Avg Resolution', '1.8 Days', Colors.orange)),
        const SizedBox(width: 12),
        Expanded(child: _buildSingleStatCard('Satisfaction', '92%', Colors.green)),
      ],
    );
  }

  Widget _buildSingleStatCard(String title, String value, Color color) {
    return Card(
      color: color.withOpacity(0.1),
      elevation: 0,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
      child: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          children: [
            Text(value, style: TextStyle(fontSize: 22, fontWeight: FontWeight.bold, color: color)),
            const SizedBox(height: 4),
            Text(title, textAlign: TextAlign.center, style: const TextStyle(fontSize: 12, color: Colors.black87)),
          ],
        ),
      ),
    );
  }

  Widget _buildCategoryPieChart() {
    return SizedBox(
      height: 200,
      child: PieChart(
        PieChartData(
          sectionsSpace: 2,
          centerSpaceRadius: 40,
          sections: [
            PieChartSectionData(value: 40, color: Colors.blue, title: 'Roads\n40%', radius: 50, titleStyle: const TextStyle(fontSize: 12, fontWeight: FontWeight.bold, color: Colors.white)),
            PieChartSectionData(value: 30, color: Colors.cyan, title: 'Water\n30%', radius: 50, titleStyle: const TextStyle(fontSize: 12, fontWeight: FontWeight.bold, color: Colors.white)),
            PieChartSectionData(value: 20, color: Colors.amber, title: 'Power\n20%', radius: 50, titleStyle: const TextStyle(fontSize: 12, fontWeight: FontWeight.bold, color: Colors.white)),
            PieChartSectionData(value: 10, color: Colors.red, title: 'Other\n10%', radius: 50, titleStyle: const TextStyle(fontSize: 12, fontWeight: FontWeight.bold, color: Colors.white)),
          ],
        ),
      ),
    );
  }

  Widget _buildDepartmentBarChart() {
    return SizedBox(
      height: 250,
      child: BarChart(
        BarChartData(
          alignment: BarChartAlignment.spaceAround,
          maxY: 100,
          barTouchData: BarTouchData(enabled: false),
          titlesData: FlTitlesData(
            show: true,
            bottomTitles: AxisTitles(
              sideTitles: SideTitles(
                showTitles: true,
                getTitlesWidget: (double value, TitleMeta meta) {
                  const style = TextStyle(fontSize: 10);
                  String text;
                  switch (value.toInt()) {
                    case 0: text = 'Roads'; break;
                    case 1: text = 'Water'; break;
                    case 2: text = 'Power'; break;
                    case 3: text = 'Sanitation'; break;
                    default: text = ''; break;
                  }
                  return SideTitleWidget(axisSide: meta.axisSide, child: Text(text, style: style));
                },
              ),
            ),
            leftTitles: const AxisTitles(sideTitles: SideTitles(showTitles: true, reservedSize: 28)),
            topTitles: const AxisTitles(sideTitles: SideTitles(showTitles: false)),
            rightTitles: const AxisTitles(sideTitles: SideTitles(showTitles: false)),
          ),
          borderData: FlBorderData(show: false),
          barGroups: [
            BarChartGroupData(x: 0, barRods: [BarChartRodData(toY: 80, color: Colors.blue, width: 16, borderRadius: BorderRadius.circular(4))]),
            BarChartGroupData(x: 1, barRods: [BarChartRodData(toY: 55, color: Colors.cyan, width: 16, borderRadius: BorderRadius.circular(4))]),
            BarChartGroupData(x: 2, barRods: [BarChartRodData(toY: 30, color: Colors.amber, width: 16, borderRadius: BorderRadius.circular(4))]),
            BarChartGroupData(x: 3, barRods: [BarChartRodData(toY: 45, color: Colors.red, width: 16, borderRadius: BorderRadius.circular(4))]),
          ],
        ),
      ),
    );
  }

  Widget _buildPerformanceMetrics() {
    return Column(
      children: [
        _buildMetricRow('SLA Compliance Rate', '88%', Colors.green),
        const Divider(),
        _buildMetricRow('Reopened Complaints', '24 this month', Colors.orange),
        const Divider(),
        _buildMetricRow('Average Citizen Rating', '4.6 / 5.0', Colors.amber),
      ],
    );
  }

  Widget _buildMetricRow(String title, String value, Color iconColor) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 8.0),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          Row(
            children: [
              Icon(Icons.analytics, color: iconColor, size: 20),
              const SizedBox(width: 8),
              Text(title, style: const TextStyle(fontSize: 16)),
            ],
          ),
          Text(value, style: const TextStyle(fontSize: 16, fontWeight: FontWeight.bold)),
        ],
      ),
    );
  }
}
