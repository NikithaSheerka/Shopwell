import 'package:flutter/cupertino.dart';

class Nutrient {
  String type;
  num value;
  String unit;
  Nutrient({this.type, this.value, this.unit});
  Color color;
  bool isDanger;
  String descr;

  Nutrient.fromJson(Map<String, dynamic> json) {
    type = json['type'] as String;
    value = ((json['value'] ?? 0) as num).ceil();
    unit = json['unit'] as String;
    isDanger = json['isDanger'] as bool;
    descr = json['descr'] as String;
  }

  Map<String, dynamic> toJson() {
    final Map<String, dynamic> data = <String, dynamic>{};
    data['type'] = type;
    data['value'] = value ?? 0;
    data['unit'] = unit;
    data['isDanger'] = isDanger;
    data['descr'] = descr;
    return data;
  }

  @override
  String toString() =>
      'Nutrient(type: $type, value: $value, unit: $unit, isDanger: $isDanger, descr: $descr)';
}
