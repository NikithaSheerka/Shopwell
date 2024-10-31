import 'package:flutter/material.dart';
import 'package:nutrigram_app/common/ui/ui_helpers.dart';
import './description_textwidget.dart';

class DProgressBar extends StatelessWidget {
  final String title;
  final String value;
  final double percent;
  final Color color;
  final bool isDanger;
  final String descr;

  const DProgressBar(
      {Key key,
      this.title,
      this.value,
      this.percent = 0,
      this.color,
      this.isDanger,
      this.descr})
      : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Column(
      children: <Widget>[
        Row(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: <Widget>[
            Row(
              children: [
                Icon(Icons.insights, size: 14, color: Colors.orange),
                SizedBox(width: 5),
                (isDanger != null)
                    ? Text(title,
                        style: Theme.of(context).textTheme.button.copyWith(
                            fontWeight: FontWeight.bold,
                            color: isDanger ? Colors.red : Colors.green))
                    : Text(title,
                        style: Theme.of(context).textTheme.button.copyWith(
                              fontWeight: FontWeight.bold,
                            ))
              ],
            ),
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Text(
                  value,
                  style: Theme.of(context).textTheme.subtitle1,
                ),
                SizedBox(width: 5),
                // ignore: prefer_if_elements_to_conditional_expressions
                (isDanger != null)
                    ? (isDanger
                        ? const Icon(Icons.circle, size: 14, color: Colors.red)
                        : const Icon(Icons.circle,
                            size: 14, color: Colors.green))
                    : SizedBox(
                        width: 5,
                      ),
              ],
            ),
          ],
        ),
        SizedBox(height: 5),
        (descr != null)
            ? Row(children: [
                DescriptionTextWidget(text: descr),
                // Text((() {
                //   if (descr != null) {
                //     return "$descr";
                //   }

                //   return "anything but true";
                // })())
              ])
            : null,
        sHeightSpan,
        Container(
          height: 6,
          width: MediaQuery.of(context).size.width,
          decoration: BoxDecoration(
            color: const Color(0xffe5e5e5).withOpacity(0.7),
            borderRadius: BorderRadius.circular(4),
          ),
          child: Row(
            children: <Widget>[
              Expanded(
                flex: (percent + 3.5).ceil().clamp(0, 100).toInt(),
                child: Container(
                  height: 6,
                  decoration: BoxDecoration(
                    color: color,
                    borderRadius: BorderRadius.circular(4),
                  ),
                ),
              ),
              Expanded(
                flex: (100 - (percent + 3.5).ceil()).clamp(0, 100).toInt(),
                child: const SizedBox.shrink(),
              ),
            ],
          ),
        ),
        mHeightSpan,
      ],
    );
  }
}
