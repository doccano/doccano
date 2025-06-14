# HTTPS settings for doccano in AWS

1. Create hosted zone in Route 53 
2. Create certificate in ACM
3. Create EC2 instance
4. Create ELB
5. Create A record in Route 53

## Create hosted zone in Route 53  

HTTPS need a domain name. If you don't have one, you can register it by the AWS Route 53 service, or you can get one from other domain seller.

After you get a domain name, you can create Hosted Zone by Route 53.

If you register domain from Route 53, you can find it in the `Hosted Zone`.

![2B0FF02C-42DA-41D1-BFA1-31018BE006ED](https://camo.githubusercontent.com/998dab1eca0e9673ab98d92b65b199cb4e2f96ea/68747470733a2f2f7773332e73696e61696d672e636e2f6c617267652f303036744b665463677931673132397a346c3733726a333131783065673078332e6a7067)

## Create certificate in ACM

![22F3520E-909A-4215-B73A-DBB452E3D4E2](https://camo.githubusercontent.com/e3e0a24d2265728072d9e65220a41d2ddd6b42bb/68747470733a2f2f7773322e73696e61696d672e636e2f6c617267652f303036744b6654636779316731326132653362306a6a3331666c3062683433312e6a7067)

You should replace the domain name by yours.

![image-20190314145326046](https://camo.githubusercontent.com/faf83a9ee1774d92a01de9f69e48ed002c7a827e/68747470733a2f2f7773312e73696e61696d672e636e2f6c617267652f303036744b66546367793167313261336a356d33756a333166393066613077342e6a7067)

![image-20190314145344449](https://camo.githubusercontent.com/874362144a3547629383ad93e1f13831e35d0b82/68747470733a2f2f7773312e73696e61696d672e636e2f6c617267652f303036744b665463677931673132613375736232626a33306b6b3039626a73762e6a7067)

![4FC120A2-6DB5-4F03-A209-12C22EDD6097](https://camo.githubusercontent.com/b75bc07e8d96b796872c697de951ab44d74d04d3/68747470733a2f2f7773342e73696e61696d672e636e2f6c617267652f303036744b665463677931673132613873643730786a3331667630686637646d2e6a7067)

Don't forget to Create record in Route 53 in step 4.

After you request a certificate, wait for a while, You should see the status become 'Issued'.

![3AAE20BC-FC34-4738-AED0-D7D67929F6FF](https://camo.githubusercontent.com/82528820652678c19ee46ff5a0f07dbfaba31f5e/68747470733a2f2f7773322e73696e61696d672e636e2f6c617267652f303036744b66546367793167313261356a776270726a333136743066387139622e6a7067)

## Create EC2 instance

In this part, you can just click the launch button to create a EC2 instance.

[![AWS CloudFormation Launch Stack SVG Button](https://cdn.rawgit.com/buildkite/cloudformation-launch-stack-button-svg/master/launch-stack.svg)](https://us-east-1.console.aws.amazon.com/cloudformation/home?region=us-east-1#/stacks/create/review?templateURL=https://s3-external-1.amazonaws.com/cf-templates-10vry9l3mp71r-us-east-1/20190732wl-new.templatexloywxxyimi&stackName=doccano)

## Create ELB

![image-20190314150439785](https://camo.githubusercontent.com/158c2fb2957546ed8bb82694497b60b9c7f38aa5/68747470733a2f2f7773332e73696e61696d672e636e2f6c617267652f303036744b6654636779316731326166376a676a746a3330663230337a3734742e6a7067)

Click the `Create Load Balancer` button and select `Application Load Balancer`.

Fill the name, change protocol to HTTPS, and do not forget add at least two availability zones. Make sure the zone that EC2 instance created is included.

![02BE83A7-4C43-48BE-BCF0-95D2DF7C603D](https://camo.githubusercontent.com/c4cc530aea78e66ea99eab905804cae66ab20a04/68747470733a2f2f7773342e73696e61696d672e636e2f6c617267652f303036744b665463677931673132616861756566736a3330796e306d6e6774732e6a7067)

Select the certificate we created early.

![image-20190314151004337](https://camo.githubusercontent.com/455140fc7b7a22a18e96e5f2aa31d9fd0e7c7722/68747470733a2f2f7773312e73696e61696d672e636e2f6c617267652f303036744b665463677931673132616b75693576366a333071763063303431382e6a7067)

You can select the same security groups created when you create the EC2 instance.

![image-20190314151110756](https://camo.githubusercontent.com/5d029d4fa494420ed077be6b57ab60935d378e7f/68747470733a2f2f7773322e73696e61696d672e636e2f6c617267652f303036744b665463677931673132616c7a796735756a33313272306139676f392e6a7067)

Or you can create a new one

![image-20190314151253917](https://camo.githubusercontent.com/e620c6738ff95f3311edf708b80a949f8b79f565/68747470733a2f2f7773312e73696e61696d672e636e2f6c617267652f303036744b665463677931673132616e736d3931706a333163313062646469652e6a7067)

Fill the target group name and leave others defualt.

![image-20190314151314109](https://camo.githubusercontent.com/f22b99c57ca9b8114683f1501942dcc3cc0874f1/68747470733a2f2f7773322e73696e61696d672e636e2f6c617267652f303036744b665463677931673132616f34797661746a3330716630666a74616d2e6a7067)

Add the instance to registered.

![image-20190314151358736](https://camo.githubusercontent.com/515649dce66466e9cefa730fc1a35a398ecb260d/68747470733a2f2f7773322e73696e61696d672e636e2f6c617267652f303036744b665463677931673132616f777667736f6a333136793066346164672e6a7067)

Then review and create.

## Create A record in Route 53

Back to route 53, and click `Create Record Set`. Fill the subname and the ELB name in the `Alias Target`.

![image-20190314151601030](https://camo.githubusercontent.com/82944e13e1ef3f4015484417a50635c9352dae33/68747470733a2f2f7773312e73696e61696d672e636e2f6c617267652f303036744b665463677931673132617231383931666a33306278306e6d6a746d2e6a7067)

Finally, you can access the doccano by HTTPS.

![image-20190314151841872](https://camo.githubusercontent.com/85dfef30b4b01df5e0d8e339b38e5a31592dd103/68747470733a2f2f7773332e73696e61696d672e636e2f6c617267652f303036744b6654636779316731326174746563636b6a3330716730396d6a73612e6a7067)
