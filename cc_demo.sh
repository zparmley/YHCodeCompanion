while [ true ]
do
	testify yelp.tests.menu.data ParentNodeTestCase.test_create_menu_node
	sleep 5
	testify yelp.tests.menu.data ParentNodeTestCase.test_create_with_children_and_items
	sleep 5
done
