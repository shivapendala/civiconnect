import 'dart:math';
import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import '../../services/offline_sync_manager.dart';

class ReportProblemScreen extends StatefulWidget {
  const ReportProblemScreen({super.key});

  @override
  State<ReportProblemScreen> createState() => _ReportProblemScreenState();
}

class _ReportProblemScreenState extends State<ReportProblemScreen> {
  int _currentStep = 0;
  final _formKey = GlobalKey<FormState>();

  // Form Data
  String? _selectedCategory;
  String? _description;
  String? _priority = 'Medium';
  bool _hasGps = false;

  void _nextStep() {
    if (_currentStep == 1 && !(_formKey.currentState?.validate() ?? false)) {
      return; // Validation failed on description
    }
    
    if (_currentStep < 5) {
      setState(() => _currentStep += 1);
    } else {
      _submitComplaint();
    }
  }

  void _prevStep() {
    if (_currentStep > 0) {
      setState(() => _currentStep -= 1);
    }
  }

  void _submitComplaint() async {
    // Generate unique ID
    final year = DateTime.now().year;
    final randomId = Random().nextInt(999999).toString().padLeft(6, '0');
    final complaintId = 'CC-$year-$randomId';

    // Queue for offline sync
    final data = {
      'id': complaintId,
      'category': _selectedCategory,
      'description': _description,
      'priority': _priority,
      'has_gps': _hasGps,
    };
    
    await OfflineSyncManager().queueOfflineAction(
      'complaints/',
      'POST',
      data,
    );

    showDialog(
      context: context,
      barrierDismissible: false,
      builder: (context) => AlertDialog(
        title: const Text('Complaint Submitted!'),
        content: Text('Your complaint has been queued for sync.\n\nID: $complaintId'),
        actions: [
          TextButton(
            onPressed: () {
              Navigator.pop(context); // Close dialog
              context.go('/home');    // Go back to home
            },
            child: const Text('OK'),
          )
        ],
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Report a Problem')),
      body: Stepper(
        type: StepperType.vertical,
        currentStep: _currentStep,
        onStepContinue: _nextStep,
        onStepCancel: _prevStep,
        steps: [
          Step(
            title: const Text('Select Category'),
            content: DropdownButtonFormField<String>(
              decoration: const InputDecoration(labelText: 'Category'),
              items: ['Pothole', 'Streetlight', 'Garbage', 'Water Leak']
                  .map((c) => DropdownMenuItem(value: c, child: Text(c)))
                  .toList(),
              onChanged: (val) => setState(() => _selectedCategory = val),
            ),
            isActive: _currentStep >= 0,
          ),
          Step(
            title: const Text('Enter Description'),
            content: Form(
              key: _formKey,
              child: TextFormField(
                maxLines: 4,
                decoration: const InputDecoration(
                  labelText: 'Description',
                  hintText: 'Provide details...',
                ),
                validator: (val) => (val == null || val.length < 10) 
                    ? 'Description must be at least 10 characters' : null,
                onChanged: (val) => _description = val,
              ),
            ),
            isActive: _currentStep >= 1,
          ),
          Step(
            title: const Text('Take Photo / Video'),
            content: Column(
              children: [
                const Icon(Icons.camera_alt, size: 64, color: Colors.grey),
                const SizedBox(height: 16),
                ElevatedButton.icon(
                  onPressed: () {},
                  icon: const Icon(Icons.add_a_photo),
                  label: const Text('Upload Media'),
                ),
                const SizedBox(height: 8),
                const Text('Max size: 10MB', style: TextStyle(color: Colors.grey)),
              ],
            ),
            isActive: _currentStep >= 2,
          ),
          Step(
            title: const Text('Get GPS Location'),
            content: Row(
              children: [
                ElevatedButton.icon(
                  onPressed: () => setState(() => _hasGps = true),
                  icon: const Icon(Icons.my_location),
                  label: const Text('Capture Location'),
                ),
                const SizedBox(width: 16),
                if (_hasGps) const Icon(Icons.check_circle, color: Colors.green),
              ],
            ),
            isActive: _currentStep >= 3,
          ),
          Step(
            title: const Text('Set Priority'),
            content: DropdownButtonFormField<String>(
              value: _priority,
              decoration: const InputDecoration(labelText: 'Priority Level'),
              items: ['Low', 'Medium', 'High', 'Critical']
                  .map((p) => DropdownMenuItem(value: p, child: Text(p)))
                  .toList(),
              onChanged: (val) => setState(() => _priority = val),
            ),
            isActive: _currentStep >= 4,
          ),
          Step(
            title: const Text('Preview & Submit'),
            content: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text('Category: ${_selectedCategory ?? "Not selected"}'),
                Text('Description: ${_description ?? "None"}'),
                Text('Priority: $_priority'),
                Text('Location Captured: ${_hasGps ? "Yes" : "No"}'),
              ],
            ),
            isActive: _currentStep >= 5,
          ),
        ],
      ),
    );
  }
}
