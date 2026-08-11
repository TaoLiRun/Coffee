# Main cafe-density robustness table

| Statistic | Paper-facing baseline | Raw 500m interaction | Log(1+) 500m interaction | Raw 1,500m interaction | Density <=3 (descriptive) | Preferred-store x event x post FE |
| --- | --- | --- | --- | --- | --- | --- |
| Focal DDD | -0.0415 | -0.0333 | -0.0392 | -0.0404 | -0.0539 | -0.0445 |
| CRV1 SE | 0.0184 | 0.0143 | 0.0176 | 0.0164 | 0.0365 | 0.0171 |
| 95% CI | [-0.0804, -0.0026] | [-0.0635, -0.0031] | [-0.0764, -0.0020] | [-0.0751, -0.0057] | [-0.1317, 0.0240] | [-0.0807, -0.0084] |
| Restricted wild p | 0.045 | 0.090 | 0.065 | 0.038 | 0.178 | 0.016 |
| Density gradient | — | 0.0300 [-0.0515, 0.1114] | 0.0079 [-0.0462, 0.0620] | -0.0122 [-0.0460, 0.0217] | — | — |
| Fitted DDD: low | — | -0.0503 at count 2.0 | -0.0445 at count 2.0 | -0.0326 at count 10.0 | — | — |
| Fitted DDD: middle | — | -0.0439 at count 5.0 | -0.0394 at count 5.0 | -0.0347 at count 23.5 | — | — |
| Fitted DDD: high | — | -0.0270 at count 13.0 | -0.0332 at count 13.0 | -0.0412 at count 65.5 | — | — |
| Observations | 99,644 | 99,644 | 99,644 | 99,644 | 41,175 | 99,644 |
| Member-events | 23,363 | 23,363 | 23,363 | 23,363 | 9,835 | 23,363 |
| Preferred stores | 101 | 101 | 101 | 101 | 37 | 101 |
| Treated stores | 18 | 18 | 18 | 18 | 9 | 18 |
| Closure clusters | 18 | 18 | 18 | 18 | 16 | 18 |
| Fixed effects | event_fe_id + rel_t + calendar_month | event_fe_id + rel_t + calendar_month | event_fe_id + rel_t + calendar_month | event_fe_id + rel_t + calendar_month | event_fe_id + rel_t + calendar_month | event_fe_id + rel_t + calendar_month + preferred_store_event_post_fe |
| Sample restriction | None | None | None | None | Preferred-store raw 500m cafe count <= 3; descriptive | Full baseline population; treated x post absorbed |
