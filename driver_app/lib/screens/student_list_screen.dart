import 'package:flutter/material.dart';
import '../models/student.dart';
import '../services/api_service.dart';

class StudentListScreen extends StatefulWidget {
  final String? busNumber;

  const StudentListScreen({super.key, this.busNumber});

  @override
  State<StudentListScreen> createState() => _StudentListScreenState();
}

class _StudentListScreenState extends State<StudentListScreen> {
  List<Student> _students = [];
  List<Student> _filteredStudents = [];
  bool _isLoading = true;
  String? _error;
  String? _selectedBoardingPoint;
  List<String> _boardingPoints = [];

  @override
  void initState() {
    super.initState();
    _loadStudents();
  }

  Future<void> _loadStudents() async {
    setState(() {
      _isLoading = true;
      _error = null;
    });

    try {
      final response = await ApiService.getStudents();
      final List<dynamic> studentsJson = response['students'] ?? [];
      
      final allStudents = studentsJson
          .map((json) => Student.fromJson(json))
          .where((student) => 
              widget.busNumber == null || 
              student.assignedBus == widget.busNumber)
          .toList();

      // Extract unique boarding points
      final points = allStudents
          .map((s) => s.boardingPoint)
          .where((p) => p.isNotEmpty)
          .toSet()
          .toList();
      points.sort();

      setState(() {
        _students = allStudents;
        _filteredStudents = allStudents;
        _boardingPoints = points;
        _isLoading = false;
      });
    } catch (e) {
      setState(() {
        _error = e.toString();
        _isLoading = false;
      });
    }
  }

  void _filterByBoardingPoint(String? point) {
    setState(() {
      _selectedBoardingPoint = point;
      if (point == null || point.isEmpty) {
        _filteredStudents = _students;
      } else {
        _filteredStudents = _students
            .where((s) => s.boardingPoint == point)
            .toList();
      }
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Students'),
        backgroundColor: Colors.green.shade700,
        foregroundColor: Colors.white,
      ),
      body: _isLoading
          ? const Center(child: CircularProgressIndicator())
          : _error != null
              ? Center(
                  child: Column(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      Icon(Icons.error_outline, size: 64, color: Colors.red.shade700),
                      const SizedBox(height: 16),
                      Text(_error!),
                      const SizedBox(height: 16),
                      ElevatedButton(
                        onPressed: _loadStudents,
                        child: const Text('Retry'),
                      ),
                    ],
                  ),
                )
              : Column(
                  children: [
                    // Filter dropdown
                    if (_boardingPoints.isNotEmpty)
                      Container(
                        padding: const EdgeInsets.all(16),
                        child: DropdownButtonFormField<String>(
                          value: _selectedBoardingPoint,
                          decoration: InputDecoration(
                            labelText: 'Filter by Boarding Point',
                            border: OutlineInputBorder(
                              borderRadius: BorderRadius.circular(12),
                            ),
                            prefixIcon: const Icon(Icons.location_on),
                          ),
                          items: [
                            const DropdownMenuItem<String>(
                              value: null,
                              child: Text('All Stops'),
                            ),
                            ..._boardingPoints.map((point) {
                              final count = _students
                                  .where((s) => s.boardingPoint == point)
                                  .length;
                              return DropdownMenuItem<String>(
                                value: point,
                                child: Text('$point ($count students)'),
                              );
                            }),
                          ],
                          onChanged: _filterByBoardingPoint,
                        ),
                      ),

                    // Student count
                    Padding(
                      padding: const EdgeInsets.symmetric(horizontal: 16),
                      child: Row(
                        mainAxisAlignment: MainAxisAlignment.spaceBetween,
                        children: [
                          Text(
                            '${_filteredStudents.length} students',
                            style: Theme.of(context).textTheme.titleMedium,
                          ),
                          Text(
                            '${_filteredStudents.where((s) => s.boarded).length} boarded',
                            style: TextStyle(
                              color: Colors.green.shade700,
                              fontWeight: FontWeight.bold,
                            ),
                          ),
                        ],
                      ),
                    ),
                    const SizedBox(height: 8),

                    // Student list
                    Expanded(
                      child: _filteredStudents.isEmpty
                          ? Center(
                              child: Column(
                                mainAxisAlignment: MainAxisAlignment.center,
                                children: [
                                  Icon(
                                    Icons.people_outline,
                                    size: 64,
                                    color: Colors.grey.shade400,
                                  ),
                                  const SizedBox(height: 16),
                                  Text(
                                    'No students found',
                                    style: TextStyle(color: Colors.grey.shade600),
                                  ),
                                ],
                              ),
                            )
                          : RefreshIndicator(
                              onRefresh: _loadStudents,
                              child: ListView.builder(
                                padding: const EdgeInsets.all(16),
                                itemCount: _filteredStudents.length,
                                itemBuilder: (context, index) {
                                  final student = _filteredStudents[index];
                                  return Card(
                                    margin: const EdgeInsets.only(bottom: 12),
                                    elevation: 2,
                                    child: ListTile(
                                      leading: CircleAvatar(
                                        backgroundColor: student.boarded
                                            ? Colors.green.shade100
                                            : Colors.grey.shade200,
                                        child: Icon(
                                          student.boarded
                                              ? Icons.check_circle
                                              : Icons.person,
                                          color: student.boarded
                                              ? Colors.green.shade700
                                              : Colors.grey.shade600,
                                        ),
                                      ),
                                      title: Text(
                                        student.name,
                                        style: const TextStyle(
                                          fontWeight: FontWeight.bold,
                                        ),
                                      ),
                                      subtitle: Column(
                                        crossAxisAlignment: CrossAxisAlignment.start,
                                        children: [
                                          const SizedBox(height: 4),
                                          Text('Roll: ${student.rollNumber}'),
                                          Text('Stop: ${student.boardingPoint}'),
                                          if (student.boarded && student.boardedAt != null)
                                            Text(
                                              'Boarded at: ${student.boardedAt}',
                                              style: TextStyle(
                                                color: Colors.green.shade700,
                                                fontSize: 12,
                                              ),
                                            ),
                                        ],
                                      ),
                                      trailing: student.boarded
                                          ? Container(
                                              padding: const EdgeInsets.symmetric(
                                                horizontal: 12,
                                                vertical: 6,
                                              ),
                                              decoration: BoxDecoration(
                                                color: Colors.green.shade100,
                                                borderRadius: BorderRadius.circular(12),
                                              ),
                                              child: Text(
                                                'BOARDED',
                                                style: TextStyle(
                                                  color: Colors.green.shade700,
                                                  fontWeight: FontWeight.bold,
                                                  fontSize: 12,
                                                ),
                                              ),
                                            )
                                          : null,
                                      isThreeLine: true,
                                    ),
                                  );
                                },
                              ),
                            ),
                    ),
                  ],
                ),
    );
  }
}
