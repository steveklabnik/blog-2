Title: Traits on Generics
Date: 2015-06-27 11:31
Modified: 2015-06-27 11:31
Category: rust
Tags: programming, rust, traits, generics
Slug: traits-on-generics
Authors: Joshua R. Rodgers
Summary: A discussion about using traits on generics in rust.

# Introduction

I've been developing quite a bit of rust lately for my project [dx-rs](https://github.com/dx-rs) which aims to be a safe
abstraction around DirectX, which uses COM (a stable ABI developed by Microsoft).  The way COM works requires my project
to have its own smart pointer type to ensure that the objects are cleaned up when they're no longer used, since COM uses
reference counting managed by the objects themselves to ensure that they are freed when they're no longer in use.

I've iterated several designs around this smart pointer over time and the design of this library has changed quite a
bit.  I've wound up heavily leveraging traits to make this type work as expected.  This type itself is generic which
means in the process, I've learned a lot of things about generics in rust in association with traits.  There was one
feature that really stuck out to me in the end, though.  That is the ability to implement traits on generics, thus
implementing the trait for an entire set of types.  Something that I find incredibly flexible and useful and not found
in the languages I typically use in my day job, like Java.  I wanted to show a few examples of how this works and why I
enjoy this feature so much.

# An Introduction to Traits

When first learning about traits, you'll usually see them used in a context very similar to interfaces in Java or C#
where the trait is used to extend a concrete type and then used as a constraint.  For this example I'm going to
introduce a trait called `PrintDebug` which looks as follows:

    :::rust
    trait PrintDebug {
        fn print_debug(&self);
    }

This trait is essentially used to extend types with a simple method to print the debug value of an instance of a type.
The typical and most basic example of this would be extending your own type, such as:

    :::rust
    #[derive(Debug)]
    struct Test;

    impl PrintDebug for Test {
        fn print_debug(&self) {
            println!("{:?}", self)
        }
    }

    fn do_stuff<T: PrintDebug>(value: &T) {
        test.print_debug();
    }

    fn main() {
        let test = Test;
        do_Stuff(&test);
    }

Which is very similar to how one would use interfaces in other languages.  Definitely a useful pattern.  The next
pattern someone learning traits might encounter is using a trait to extend another type, which is not a part of their
own crate.  This typically goes like:

    :::rust
    impl PrintDebug for i32 {
        fn print_debug(&self) {
            println!("{:?}", self)
        }
    }

Again, an incredibly useful pattern and very similar to extension methods in C#.

The problem here, is that both these implementations are restricted to a single type and would have to end up
implementing this trait on every type you need the trait for by hand.  For certain sets of types (e.g. all `Debug`
types) this can be a lot of implementations and not even feasible, because the set of these types cannot be known at
compile time by the developer.  This is where generics to the rescue!

# Generics and Traits, Best Friends Forever

Generics and traits truly are best friends forever.  They work together to achieve some great things. I want to show
some examples of why this is.

Let's say I wanted to implement `PrintDebug` on every type that also implemented `Debug`.  That's not feasible to do by
hand for reasons outlined earlier.  So, how do I do this?  Well, you can implement traits on generics! For example:

    :::rust
    impl<T: Debug> PrintDebug for T {
        fn print_debug(&self) {
            println!("{:?}", self)
        }
    }

See what I did there?  I declared a generic parameter on the `impl`, constrained it to `Debug` types, and then
implemented `PrintDebug` on the generic parameter `T`.  I find this incredibly cool.  This would be very similar to
implementing an extension method on an `IDebug` interface in C#.  It's a huge time saver and for writing your own
libraries it allows you to ensure all the types in your crate and any crate that uses your crate with types that meet
your constraints will end up implementing this trait.  Of course, this means there has to be some rules about how these
sort of implementations must work.  These rules are known as trait coherence (I'll describe this in a future post). So
this sort of implementation won't work in some scenarios, but as long as the trait is a trait you declared in your crate
, you can rest easy knowing that you have full control over how that trait will get implemented on types.

You can even use this pattern to extend types which take a generic parameter.  Drawing an example from my own work,
we'll use a struct called `ComPtr` which is a generic.  I won't describe this type in-depth, but I'll write a short
example of using this pattern on a generic struct.

    :::rust
    impl<T> Deref for ComPtr<T> {
        type Target = T;

        fn deref(&self) -> &T {
            self.inner
        }
    }

Here I implemented a built-in trait `Deref` on all `ComPtr<T>` types.  Incredibly useful pattern, for sure!  Of course
you can also use constraints on the generic parameters to implement the trait for a subset of `ComPtr<T>` types where
`T` meets the specific traits.  An example of this would be:

    :::rust
    unsafe impl<T: Send> Send for ComPtr<T> {}

Here I've implemented `Send` on `ComPtr<T>` if and only if `T` is also `Send`.  Which means `ComPtr<T>` is only
`Send`able if `T` itself is `Send`able.  We can ignore the `unsafe` portion for now, I'll look into blogging about this
in the future.

So far all the examples I've demonstrated are very similar to C# extension methods.  However, there's still more to show
when it comes to traits and generics in Rust.

For example, let's say I have two traits in my crate defined as (note, these are abridged examples):

    :::rust
    trait Serializable {}

    trait Serialize {
        fn serialize(&self) -> String;
    }

I could then do a generic implementation along the lines of:

    :::rust
    impl<T: Serializable> Serialize for T {
        fn frobulate(&self) -> String {
            //Serilization happens here!
        }
    }

So far, this isn't really too different from my other examples, but what if I implement `Frobulable` on `i32`?

    ::rust
    impl Serializable for i32 {}

Well now... suddenly a built-in type like i32 is extended to be `Serializable`.  As long as `i32` meets the requirements
to be serialized by the blanket implementation of `Serialize`, then everything is great!  What if `i32` doesn't meet
those requirements?  We could still just implement `Serialize` directly on `i32` without implementing `Serializable` and
`i32` will now still be a `Serialize` type.

So with this in mind, what's so special about this?  First off, unlike extension methods in C# which only extend a type
with more methods and not the type itself, traits can essentially extend arbitrary types (again, there's trait coherence
restrictions).  That means any `impl` of a trait on any given type extends that type not only with the methods of that
trait, but includes that type in the set of types that trait represents.  So traits are more than extension methods.
They're extension types.  So you can use traits to extend other traits, which can extend other types.  It's traits all
the way down.

# A Final Word

I find traits in rust to be incredibly useful in designing libraries and all the different features of traits allow you
to do some really useful abstractions.  I plan to continue talking about other features of traits and their uses in the
future.  Topics I would like to cover include:

* Trait coherence
* Associated items (associated types, consts [future version of rust], etc)
* Default implementations of methods
* Unsafe traits

This was my first ever programming blog post.  I certainly will appreciate any feedback so I can improve my abilities to
write about these sort of topics.
