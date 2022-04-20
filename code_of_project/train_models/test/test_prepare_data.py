from sklearn.model_selection import train_test_split
from code_of_project.helper_methods import cast_to_pandas, load_obj


def prepare_dataset(args):
    raw_df = load_obj(path=args.path_to_dataset)

    train_df, train_labels, val_features, val_labels, test_df, test_labels, feature_columns = \
        create_train_val_test_data(raw_df, args)

    return train_df, train_labels, val_features, val_labels, test_df, test_labels, feature_columns


def create_train_val_test_data(cleaned_df, args):
    # Use a utility from sklearn to split and shuffle your dataset.
    train_df, test_df = train_test_split(cleaned_df, test_size=0.2)
    train_df, val_df = train_test_split(train_df, test_size=0.2)

    # Form np arrays of labels and features.
    train_labels = train_df.pop(args.label_category)
    val_labels = val_df.pop(args.label_category)
    test_labels = test_df.pop(args.label_category)
    # test_labels_one_hot, train_labels_one_hot, val_labels_one_hot = cast_to_hot_label(test_labels, train_labels,
    #                                                                                   val_labels)
    feature_columns = list(train_df.columns)

    print('Training labels shape:', train_labels.shape)
    print('Validation labels shape:', val_labels.shape)
    print('Test labels shape:', test_labels.shape)
    print('Training features shape:', train_df.shape)
    print('Validation features shape:', val_df.shape)
    print('Test features shape:', test_df.shape)
    return train_df, train_labels, val_df, val_labels, test_df, test_labels, feature_columns

